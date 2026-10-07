"""Run in a disposable Blender configuration: --python this_file -- KIND ZIP OUTPUT.

Only test-managed preferences are modified. No global Python path manipulation is
used: installation and module discovery are performed by Blender itself.
"""
import importlib
import json
import os
from pathlib import Path
import sys

import addon_utils
import bpy


arguments = sys.argv[sys.argv.index('--') + 1:]
kind, archive, output = arguments[:3]
phase = arguments[3] if len(arguments) > 3 else 'install'
existing = phase != 'install'
output = Path(output)
output.mkdir(parents=True, exist_ok=True)
if existing:
    if phase == 'reenable':
        saved = json.loads((output / 'report.json').read_text(encoding='utf-8'))
        addon_utils.enable(saved['package'], default_set=True)
elif kind == 'extension':
    repo = bpy.context.preferences.extensions.repos.new(name='FreeMoCap test', module='freemocap_test',
                                                       custom_directory=os.environ.get('FREEMOCAP_BLENDER_TEST_REPOSITORY', str(output / 'repository')))
    repo.use_remote_url = False
    result = bpy.ops.extensions.package_install_files(filepath=str(Path(archive).resolve()),
                                                      repo=repo.module, enable_on_install=True)
    assert result == {'FINISHED'}, result
else:
    bpy.ops.preferences.addon_install(filepath=str(Path(archive).resolve()), overwrite=True)
    addon_utils.enable('freemocap_blender_addon', default_set=True)
# addon_utils.modules returns metadata-only modules, not executed packages.
modules = [importlib.import_module(name) for name in bpy.context.preferences.addons.keys()
           if name.split('.')[-1] == 'freemocap_blender_addon']
assert len(modules) == 1, [m.__name__ for m in modules]
module = modules[0]
package = module.__name__
assert package in bpy.context.preferences.addons, 'Registration failed'
# Exercise registration hooks before binary imports. Blender's wheel manager has
# separate disable/re-enable tests across process boundaries below.
module.unregister()
assert not hasattr(bpy.types.Scene, 'freemocap_properties')
module.register()
assert hasattr(bpy.types.Scene, 'freemocap_properties')
dependencies = importlib.import_module(package + '.utilities.dependencies')
report = dependencies.dependency_report()
assert dependencies.require_module('tomli').loads('example = 1')['example'] == 1
arrow = dependencies.require_module('pyarrow')
parquet = dependencies.parquet_module()
sample = output / 'parquet round trip.parquet'
table = arrow.table(dict(frame_number=[0, 1], value=[1.25, None]))
parquet.write_table(table, sample, compression='zstd')
assert parquet.read_table(sample).equals(table)
assert dependencies.load_toml(Path(__file__).parents[1] / 'pyproject.toml')['project']['name'] == 'freemocap_blender_addon'
# Verify the public API through an installed package, without running the scene pipeline.
api = importlib.import_module(package + '.export_api')
try:
    api.export_recording(recording_path=output / 'absent', blend_file_path=output / 'out.blend')
except ValueError:
    pass
else:
    raise AssertionError('Invalid recording accepted')
report.update(package=package, blender=list(bpy.app.version), parquet_roundtrip=True,
              register_twice=True, export_preflight=True, restarted=existing)
# Exercise dispatch with a controlled scene writer, not the recording loader.
main_module = importlib.import_module(package + '.main')
original = main_module.ajc27_run_as_main_function
configuration = object()
recording = output / 'recording with spaces'
recording.mkdir(exist_ok=True)
def scene_writer(recording_path, blend_file_path, config):
    assert Path(recording_path) == recording.resolve()
    assert config is configuration
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
try:
    main_module.ajc27_run_as_main_function = scene_writer
    api.export_recording(recording_path=recording, blend_file_path=output / 'dispatch test.blend', config=configuration)
finally:
    main_module.ajc27_run_as_main_function = original
report['controlled_export_dispatch'] = True
legacy_timing = importlib.import_module(package + '.core_functions.setup_scene.set_start_end_frame')
legacy_timing.set_start_end_frame(10)
assert (bpy.context.scene.frame_start, bpy.context.scene.frame_end) == (0, 9)
legacy_timing.set_scene_framerate(59.94)
assert abs(bpy.context.scene.render.fps / bpy.context.scene.render.fps_base - 59.94) < 1e-4
# Check actual animation primitives against synthetic and prepared recording data.
spec = importlib.util.spec_from_file_location('scene_checks', Path(__file__).with_name('blender_scene_checks.py'))
scene_checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scene_checks)
checks, references = scene_checks.build_checks(package, parquet, include_references=phase == 'install')
scene_file = output / ('animation ' + phase + '.blend')
bpy.ops.wm.save_as_mainfile(filepath=str(scene_file.resolve()))
bpy.ops.wm.open_mainfile(filepath=str(scene_file.resolve()))
scene_checks.assert_locations(checks)
report.update(animation_evaluation=True, animation_reopen=True, reference_checks=references)
if phase == 'install':
    spec = importlib.util.spec_from_file_location('parquet_contract', Path(__file__).with_name('blender_parquet_contract.py'))
    parquet_contract = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parquet_contract)
    report['parquet_contract_checks'] = parquet_contract.run(package, output)
    spec = importlib.util.spec_from_file_location('parquet_checks', Path(__file__).with_name('blender_parquet_checks.py'))
    parquet_checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parquet_checks)
    report['parquet_loader_checks'] = parquet_checks.build_checks(package, output)
(output / (phase + '-report.json' if existing else 'report.json')).write_text(json.dumps(report, indent=2), encoding='utf-8')
if phase == 'disable':
    addon_utils.disable(package, default_set=True)
    assert package not in bpy.context.preferences.addons
bpy.ops.wm.save_userpref()
print('FREEMOCAP_SMOKE_PASS ' + json.dumps(report))
