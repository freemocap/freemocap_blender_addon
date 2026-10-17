"""Test source sync, the installed editor's reload operator, and both exports.

Uses a disposable copy of a prepared development stage and core's accepted test
publication. Does not start VS Code's debugger/server or install its dependencies.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from tools import develop, reference_data, test_blender_package


def run(state_path, vscode_extension, prepared_root):
    state = json.loads(Path(state_path).read_text(encoding='utf-8'))
    operator = Path(vscode_extension) / 'pythonFiles/include/blender_vscode/operators/addon_update.py'
    if not operator.is_file():
        raise ValueError('Cannot find installed JacquesLucke reload operator: ' + str(operator))
    output = Path(tempfile.mkdtemp(prefix='development-test-', dir=develop.ROOT / '.test-artifacts'))
    reference = reference_data.snapshot(Path(prepared_root), 'test_data', output / 'references')
    with tempfile.TemporaryDirectory(prefix='fmc-devtest-') as directory:
        stage = Path(directory)
        original = Path(state['stage']) / 'user/scripts/addons'
        shutil.copytree(original, stage / 'user/scripts/addons')
        state['stage'] = str(stage)
        disposable_state = stage / 'state.json'
        disposable_state.write_text(json.dumps(state), encoding='utf-8')
        (stage / 'development-owner.json').write_text(json.dumps(dict(repository=str(develop.ROOT), state=str(disposable_state.resolve()))))
        environment = test_blender_package.isolated_environment(stage / 'user')
        command = [state['blender'], '--background', '--factory-startup', '--python-exit-code', '1',
                   '--python', str(develop.ROOT / 'tests/blender_development_smoke.py'), '--',
                   str(disposable_state), str(operator.resolve()), sys.executable, reference['path'], str(output)]
        with (output / 'blender.log').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=stage, env=environment, stdout=log, stderr=subprocess.STDOUT, timeout=300)
        reference_data.verify_unchanged([reference])
        if result.returncode or 'FREEMOCAP_DEVELOPMENT_PASS ' not in (output / 'blender.log').read_text(encoding='utf-8', errors='replace'):
            raise RuntimeError('Development test failed; inspect ' + str(output / 'blender.log'))
    print((output / 'development-report.json').read_text())
    print('Development test reports: ' + str(output))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--vscode-extension', type=Path, required=True)
    parser.add_argument('--prepared-root', type=Path, default=Path.home() / 'freemocap_data/testing/prepared')
    args = parser.parse_args()
    run(args.state, args.vscode_extension, args.prepared_root)
