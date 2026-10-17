"""Compatibility entry point for the host-only builder shipped in the dependency."""
import importlib.util
from pathlib import Path
import sys

path = Path(__file__).resolve().parents[1] / 'freemocap_blender_addon/_host_tools/build_addon.py'
spec = importlib.util.spec_from_file_location(__name__, path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules[__name__] = module

if __name__ == '__main__':
    module.main()
