"""Build-time template: shipped ONLY in legacy add-on archives, never Extensions.

Legacy Blender has no wheel manager. Dependencies are expanded by the builder,
never by this module. A temporary search path loads the private dependency; an
already loaded foreign copy is rejected rather than replaced. Nothing is written.
"""
import importlib
import json
import platform
import sys


def load_module(name, root):
    metadata = json.loads((root / "_legacy_dependencies.json").read_text(encoding="utf-8"))
    machine = platform.machine().lower()
    machine = {"amd64": "x86_64", "aarch64": "arm64"}.get(machine, machine)
    actual = [platform.system(), machine, "{}.{}".format(*sys.version_info[:2])]
    if actual != metadata["runtime"]:
        raise RuntimeError("Legacy dependency package targets {}, running {}".format(metadata["runtime"], actual))
    vendor = (root / "_dependencies").resolve()
    top = name.split(".")[0]
    loaded = sys.modules.get(top)
    if loaded is not None:
        try:
            from pathlib import Path
            Path(loaded.__file__).resolve().relative_to(vendor)
        except (AttributeError, TypeError, ValueError):
            raise RuntimeError("{} is already loaded from another package; restart Blender without that dependency conflict".format(top))
    before = list(sys.path)
    try:
        sys.path.insert(0, str(vendor))
        return importlib.import_module(name)
    finally:
        sys.path[:] = before
