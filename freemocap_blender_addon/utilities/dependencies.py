"""Offline dependency access, shared by UI and background export.

Extensions receive wheels from Blender. Only a legacy distribution contains the
private legacy loader. No import attempts to install or repair an environment.
"""
import importlib
from pathlib import Path


class DependencyUnavailable(RuntimeError):
    pass


def require_module(name):
    if name not in ("pyarrow", "pyarrow.parquet", "tomli"):
        raise ValueError("Unsupported optional dependency: " + name)
    root = Path(__file__).resolve().parents[1]
    try:
        if (root / "_legacy_dependencies.json").is_file():
            from .legacy_dependencies import load_module
            return load_module(name, root)
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name.split('.')[0]:
            raise DependencyUnavailable(
                "Missing {} in Blender's Python. The add-on code is present, but its dependency is not. "
                "Install the complete FreeMoCap ZIP. For VS Code source development, run "
                "python -B -m tools.develop prepare --blender <blender-executable>, then open "
                "the generated .code-workspace. No packages were downloaded or installed.".format(exc.name)
            ) from exc
        raise DependencyUnavailable(
            "The {} dependency is incomplete: {}. Reinstall the complete package for this Blender. "
            "No packages were downloaded or installed.".format(name, exc)
        ) from exc
    except (ImportError, OSError, RuntimeError) as exc:
        raise DependencyUnavailable(
            "Cannot initialize {} in Blender's Python (binary compatibility or dependency conflict). Install the FreeMoCap package "
            "built for this Blender Python version and operating system. "
            "No packages were downloaded or installed. Details: {}".format(name, exc)
        ) from exc


def parquet_module():
    return require_module("pyarrow.parquet")


def load_toml(path):
    try:
        import tomllib
    except ImportError:
        tomllib = require_module("tomli")
    with open(path, "rb") as stream:
        return tomllib.load(stream)


def dependency_report():
    """Actually import binary modules; finding a module spec is insufficient."""
    import platform
    import sys
    arrow = require_module("pyarrow")
    parquet_module()
    return dict(python=sys.version, platform=platform.platform(),
                machine=platform.machine(), pyarrow=arrow.__version__,
                pyarrow_path=str(arrow.__file__))
