"""Test a built package in an explicitly selected Blender, with disposable preferences.

Example: python -B tools/test_blender_package.py --blender /path/to/blender
  --kind extension --archive dist/package.zip
Reports/logs are retained under ignored .test-artifacts; nothing is installed in
the user's Blender configuration. This does not validate recording reconstruction.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(blender, kind, archive):
    artifacts = ROOT / '.test-artifacts'
    artifacts.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='blender-smoke-', dir=artifacts))
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    resources = output / 'user'
    environment['BLENDER_USER_RESOURCES'] = str(resources)
    # Explicit old-version variables avoid relying on the newer resources override.
    for variable, folder in [('BLENDER_USER_CONFIG', 'config'), ('BLENDER_USER_SCRIPTS', 'scripts'),
                             ('BLENDER_USER_DATAFILES', 'datafiles'), ('BLENDER_USER_EXTENSIONS', 'extensions')]:
        path = resources / folder
        path.mkdir(parents=True, exist_ok=True)
        environment[variable] = str(path)
    for phase in ('install', 'restart', 'disable', 'reenable'):
        command = [str(blender), '--background', '--python-exit-code', '1']
        if phase == 'install':
            command += ['--factory-startup']
        if kind == 'extension':
            command += ['--offline-mode']
        command += ['--python', str(ROOT / 'tests/blender_package_smoke.py'), '--', kind,
                    str(archive.resolve()), str(output)]
        if phase != 'install':
            command += [phase]
        with (output / (phase + '.log')).open('w', encoding='utf-8') as log:
            result = subprocess.run(command, env=environment, stdout=log, stderr=subprocess.STDOUT, timeout=300)
        if result.returncode:
            raise RuntimeError('Blender {} failed ({}); inspect {}'.format(phase, result.returncode, output))
    print((output / 'reenable-report.json').read_text(encoding='utf-8'))
    print('Reports: ' + str(output))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', type=Path, required=True)
    parser.add_argument('--kind', choices=('legacy', 'extension'), required=True)
    parser.add_argument('--archive', type=Path, required=True)
    run(**vars(parser.parse_args()))
