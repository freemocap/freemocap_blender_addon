"""Generate reproducible build provenance; no commits, tags, or network access."""
import importlib.util
import hashlib
import json
import subprocess
from pathlib import Path


def identity_module(root):
    spec = importlib.util.spec_from_file_location('fmc_build_identity', Path(root) / 'freemocap_blender_addon/build_identity.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_identity(*, root, package, version, kind, python, platform):
    module = identity_module(root)
    def git(*args):
        try:
            return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL).decode().strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    commit = git('rev-parse', 'HEAD')
    status = git('status', '--porcelain', '--untracked-files=normal')
    identity = dict(schema_version=1, source_hash_version=1, version=version,
        export_api_version=module.EXPORT_API_VERSION, source_commit=commit,
        source_dirty=bool(status) if status is not None else None,
        source_sha256=module.source_hash(package), package_format=kind,
        python=python, platform=platform,
        dependency_lock_sha256=hashlib.sha256((package / 'dependency-lock.json').read_bytes()).hexdigest())
    (package / 'build-info.json').write_text(json.dumps(identity, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    return identity
