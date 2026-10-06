"""Real Blender + installed VS Code extension's reload operator, without servers.

The operator class is executed unchanged from the user's installed extension.
Only its editor notification/redraw hooks are replaced. No debugger packages,
network service, or VS Code window is needed for this lifecycle regression test.
"""
import ast
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import traceback

import bpy

state_path, operator_path, host_python, reference, output = sys.argv[sys.argv.index('--') + 1:]
state = json.loads(Path(state_path).read_text())
stage = Path(state['stage'])
package = 'freemocap_blender_addon'
bpy.ops.preferences.addon_refresh()
assert bpy.ops.preferences.addon_enable(module=package) == {'FINISHED'}
deps = importlib.import_module(package + '.utilities.dependencies')
arrow = deps.require_module('pyarrow')
original_arrow = id(arrow)
before = deps.dependency_report()
assert str(stage) in before['pyarrow_path']
tree = ast.parse(Path(operator_path).read_text(encoding='utf-8'))
operator = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'UpdateAddonOperator')
namespace = dict(bpy=bpy, sys=sys, traceback=traceback, StringProperty=bpy.props.StringProperty,
                 send_dict_as_json=lambda message: print('EDITOR_NOTIFICATION', message), redraw_all=lambda: None)
exec(compile(ast.Module(body=[operator], type_ignores=[]), operator_path, 'exec'), namespace)
bpy.utils.register_class(namespace['UpdateAddonOperator'])
# Write only inside the managed staging directory to demonstrate that the
# pre-reload build task restores source changes, without altering the checkout.
staged_module = stage / 'user/scripts/addons' / package / 'utilities/dependencies.py'
staged_module.write_text(staged_module.read_text() + '\nDEVELOPMENT_STALE_SENTINEL = True\n')
subprocess.run([host_python, '-B', '-m', 'tools.develop', 'sync', '--state', state_path],
               cwd=Path(__file__).resolve().parents[1], check=True)
assert 'DEVELOPMENT_STALE_SENTINEL' not in staged_module.read_text()
for revision in range(2):
    staged_module.write_text(staged_module.read_text() + '\nDEVELOPMENT_RELOAD_SENTINEL = {}\n'.format(revision))
    assert bpy.ops.dev.update_addon(module_name=package) == {'FINISHED'}
    deps = importlib.import_module(package + '.utilities.dependencies')
    assert deps.DEVELOPMENT_RELOAD_SENTINEL == revision
    assert id(deps.require_module('pyarrow')) == original_arrow
    assert deps.parquet_module() is not None
# Both actual CLI export routes run after source reload, using a prepared copy.
spec = importlib.util.spec_from_file_location('export_runner', Path(__file__).parents[1] / 'tools/blender_export.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
outputs = []
for route in ('parquet_segments', 'parquet_constraints'):
    path = Path(output) / (route + '.blend')
    runner.main([package, reference, str(path), '--route', route])
    assert path.stat().st_size > 0
    outputs.append(str(path))
report = dict(runtime=state['runtime'], dependency=before, source_sync=True, source_code_reloaded=True, same_process_reloads=2,
              reload_operator=str(operator_path), operator_sha256=hashlib.sha256(Path(operator_path).read_bytes()).hexdigest(),
              background_exports=outputs)
(Path(output) / 'development-report.json').write_text(json.dumps(report, indent=2))
print('FREEMOCAP_DEVELOPMENT_PASS ' + json.dumps(report))
