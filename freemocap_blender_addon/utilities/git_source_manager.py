"""Git-source dependency manager for Blender addons.

Clones, fetches, and updates git repositories to a local cache directory,
returning paths suitable for ``sys.path`` injection.  Uses only the stdlib
so it can run inside Blender's bundled Python before any dependencies are
installed.

Usage::

    from freemocap_blender_addon.utilities.git_source_manager import resolve_git_sources

    sources = [
        {"git": "https://github.com/freemocap/skellytracker", "branch": "development"},
        {"git": "https://github.com/freemocap/skellycam", "branch": "development"},
    ]
    for p in resolve_git_sources(sources):
        sys.path.insert(0, str(p))

Cache directory
---------------
Default: ``~/.cache/freemocap/git_sources/``
Override: set ``FREEMOCAP_GIT_SOURCES_DIR`` environment variable.

Lock file
---------
``.source_lock.json`` in the cache directory records the last-seen commit
for each dependency.  On subsequent runs the manager fetches the remote
branch and compares — if HEAD has moved it pulls, otherwise it skips.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


# ── Public API ────────────────────────────────────────────────────────

def resolve_git_sources(sources: list[dict[str, str]]) -> list[Path]:
    """Ensure *sources* are cloned & up-to-date; return their repo-root paths.

    Each source dict must have:
        ``"git"`` — the clone URL (e.g. ``"https://github.com/freemocap/skellycam"``)
        ``"branch"`` — the branch to track (e.g. ``"development"``)

    Returns the same number of paths as *sources*, in the same order.
    """
    cache_dir = _cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)
    lock_file = cache_dir / ".source_lock.json"
    lock_data = _read_json(lock_file)

    paths: list[Path] = []
    for spec in sources:
        git_url = spec["git"]
        branch = spec.get("branch", "main")
        repo_name = _repo_name(git_url)
        repo_path = cache_dir / repo_name

        new_head = _sync(repo_path, git_url, branch)
        lock_data[repo_name] = {
            "git": git_url,
            "branch": branch,
            "head": new_head,
        }
        paths.append(repo_path)

    _write_json(lock_file, lock_data)
    return paths


# ── Internal helpers ──────────────────────────────────────────────────

def _cache_dir() -> Path:
    """Resolve the cache directory (env-var override or XDG default)."""
    if env := os.environ.get("FREEMOCAP_GIT_SOURCES_DIR"):
        return Path(env)
    # XDG_CACHE_HOME → ~/.cache
    xdg = os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))
    return Path(xdg) / "freemocap" / "git_sources"


def _repo_name(git_url: str) -> str:
    """Extract a directory name from a git URL.

    >>> _repo_name("https://github.com/freemocap/skellycam")
    'skellycam'
    >>> _repo_name("git@github.com:freemocap/skellycam.git")
    'skellycam'
    """
    url = git_url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    return url.rsplit("/", 1)[-1].rsplit(":", 1)[-1]


def _sync(repo_path: Path, git_url: str, branch: str) -> str:
    """Clone or update *repo_path* and return the current HEAD sha."""
    if repo_path.is_dir() and (repo_path / ".git").is_dir():
        return _update(repo_path, branch)
    else:
        return _clone(repo_path, git_url, branch)


# ── Git operations ────────────────────────────────────────────────────

def _clone(repo_path: Path, git_url: str, branch: str) -> str:
    """Clone *git_url* @ *branch* into *repo_path*; return HEAD sha."""
    print(f"[git_source] cloning {_repo_name(git_url)} …")
    _run_git(
        ["clone", "--branch", branch, "--single-branch", git_url, str(repo_path)],
        cwd=None,
    )
    return _rev_parse(repo_path, "HEAD")


def _update(repo_path: Path, branch: str) -> str:
    """Fetch *branch*, fast-forward if behind, return HEAD sha."""
    repo_name = repo_path.name

    # Fetch the tracked branch
    try:
        _run_git(["fetch", "origin", branch], cwd=repo_path)
    except subprocess.CalledProcessError:
        print(f"[git_source] {repo_name}: fetch failed (offline?), using cached copy")
        return _rev_parse(repo_path, "HEAD")

    local_head = _rev_parse(repo_path, "HEAD")
    remote_head = _rev_parse(repo_path, f"origin/{branch}")

    if local_head == remote_head:
        print(f"[git_source] {repo_name}: up to date  ({local_head[:8]})")
        return local_head

    print(f"[git_source] {repo_name}: updating  {local_head[:8]} → {remote_head[:8]}")

    # Check for local changes that would prevent fast-forward
    status = _run_git(["status", "--porcelain"], cwd=repo_path).strip()
    if status:
        print(f"[git_source] {repo_name}: WARNING — local changes detected, "
              f"stashing before pull")
        _run_git(["stash", "--include-untracked"], cwd=repo_path)

    _run_git(["checkout", branch], cwd=repo_path)
    _run_git(["pull", "--ff-only", "origin", branch], cwd=repo_path)
    return _rev_parse(repo_path, "HEAD")


# ── Plumbing ──────────────────────────────────────────────────────────

def _run_git(args: list[str], cwd: Path | None = None) -> str:
    """Run a git command and return stdout, or raise on failure."""
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        cmd_str = " ".join(["git"] + args)
        raise subprocess.CalledProcessError(
            result.returncode, cmd_str,
            output=result.stdout, stderr=result.stderr,
        )
    return result.stdout


def _rev_parse(repo_path: Path, ref: str) -> str:
    """Return the commit sha for *ref* (e.g. ``HEAD``, ``origin/main``)."""
    return _run_git(["rev-parse", ref], cwd=repo_path).strip()


def _read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file, returning an empty dict if it doesn't exist."""
    if path.is_file():
        return json.loads(path.read_text())
    return {}


def _write_json(path: Path, data: dict[str, Any]) -> None:
    """Atomically write *data* as JSON."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)


# ── CLI (for testing outside Blender) ─────────────────────────────────

if __name__ == "__main__":
    test_sources = [
        {"git": "https://github.com/freemocap/skellylogs", "branch": "main"},
    ]
    print(f"Cache dir: {_cache_dir()}")
    for p in resolve_git_sources(test_sources):
        print(f"  → {p}")
    print("Done.")
