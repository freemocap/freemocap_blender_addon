"""Blender --background --python-exit-code 1 --python this_file -- PACKAGE INPUT OUTPUT.

PACKAGE is the exact installed/enabled add-on name, including the Blender-chosen
extension repository namespace when applicable. This script never installs one.
"""
import importlib
import sys


def main(arguments):
    if len(arguments) != 3:
        raise ValueError("Expected installed package name, recording directory, and .blend output")
    package, recording, output = arguments
    import bpy
    if package not in bpy.context.preferences.addons:
        raise RuntimeError("Enable the installed FreeMoCap add-on before exporting: " + package)
    module = importlib.import_module(package)
    if not getattr(module, "__freemocap_export_api__", False):
        raise ValueError("Selected package does not expose the FreeMoCap export API")
    api = importlib.import_module(package + ".export_api")
    return api.export_recording(recording_path=recording, blend_file_path=output)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:])
