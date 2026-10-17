"""Blender --background --python-exit-code 1 --python this_file -- PACKAGE INPUT OUTPUT.

PACKAGE is the exact installed/enabled add-on name, including the Blender-chosen
extension repository namespace when applicable. This script never installs one.
"""
import importlib
import argparse
import sys
import json
from pathlib import Path


def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package')
    parser.add_argument('recording')
    parser.add_argument('output')
    parser.add_argument('--route', choices=('legacy_npy', 'parquet_segments', 'parquet_constraints'), default='legacy_npy')
    parser.add_argument('--trajectory-channel', choices=('LANDMARKS_3D', 'MAPPED_KEYPOINTS_3D'), default='LANDMARKS_3D')
    parser.add_argument('--run-id', type=int)
    parser.add_argument('--sensor-group')
    parser.add_argument('--config', type=Path, help='JSON file containing add-on configuration sections')
    args = parser.parse_args(arguments)
    package, recording, output = args.package, args.recording, args.output
    import bpy
    if package not in bpy.context.preferences.addons:
        raise RuntimeError("Enable the installed FreeMoCap add-on before exporting: " + package)
    module = importlib.import_module(package)
    if not getattr(module, "__freemocap_export_api__", False):
        raise ValueError("Selected package does not expose the FreeMoCap export API")
    api = importlib.import_module(package + ".export_api")
    return api.export_recording(recording_path=recording, blend_file_path=output, route=args.route,
                                trajectory_channel=args.trajectory_channel, run_id=args.run_id,
                                sensor_group=args.sensor_group,
                                config=json.loads(args.config.read_text(encoding='utf-8')) if args.config else None)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:])
