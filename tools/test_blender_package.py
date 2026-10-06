"""Test a built package in an explicitly selected Blender, with disposable preferences.

Example: python -B tools/test_blender_package.py --blender /path/to/blender
  --kind extension --archive dist/package.zip
Reports/logs are retained under ignored .test-artifacts; nothing is installed in
the user's Blender configuration. Prepared references exercise both Parquet
loading routes, animation evaluation, and saved-scene reloads.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def isolated_environment(resources):
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    # Do not let the launching shell's Python environment supply dependencies.
    environment.pop('PYTHONPATH', None)
    environment.pop('PYTHONHOME', None)
    environment['PYTHONNOUSERSITE'] = '1'
    environment['BLENDER_USER_RESOURCES'] = str(resources)
    # Explicit old-version variables avoid relying on the newer resources override.
    for variable, folder in [('BLENDER_USER_CONFIG', 'config'), ('BLENDER_USER_SCRIPTS', 'scripts'),
                             ('BLENDER_USER_DATAFILES', 'datafiles'), ('BLENDER_USER_EXTENSIONS', 'extensions')]:
        path = resources / folder
        path.mkdir(parents=True, exist_ok=True)
        environment[variable] = str(path)
    return environment


def run(blender, kind, archive, output=None, references=None):
    # Deep repository paths can exceed Win32's extraction limit. Keep installed
    # test packages short-lived in system temp; retain reports in the repository.
    with tempfile.TemporaryDirectory(prefix='fmc-') as temporary:
        return _run(blender, kind, archive, output, references, Path(temporary))


def _run(blender, kind, archive, output, references, resources):
    artifacts = ROOT / '.test-artifacts'
    artifacts.mkdir(exist_ok=True)
    output = Path(output) if output is not None else Path(tempfile.mkdtemp(prefix='blender-smoke-', dir=artifacts))
    output.mkdir(parents=True, exist_ok=True)
    environment = isolated_environment(resources)
    environment['FREEMOCAP_BLENDER_TEST_REPOSITORY'] = str(resources / 'repository')
    environment.pop('FREEMOCAP_BLENDER_REFERENCE_MANIFEST', None)
    if references is not None:
        environment['FREEMOCAP_BLENDER_REFERENCE_MANIFEST'] = str(references)
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
            result = subprocess.run(command, env=environment, stdout=log, stderr=subprocess.STDOUT, timeout=900)
        if result.returncode:
            raise RuntimeError('Blender {} failed ({}); inspect {}'.format(phase, result.returncode, output))
        report = output / ('report.json' if phase == 'install' else phase + '-report.json')
        if not report.is_file() or 'FREEMOCAP_SMOKE_PASS ' not in (output / (phase + '.log')).read_text(encoding='utf-8', errors='replace'):
            raise RuntimeError('Blender {} exited without completing checks; inspect {}'.format(phase, output))
    print((output / 'reenable-report.json').read_text(encoding='utf-8'))
    print('Reports: ' + str(output))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', type=Path, required=True)
    parser.add_argument('--kind', choices=('legacy', 'extension'), required=True)
    parser.add_argument('--archive', type=Path, required=True)
    run(**vars(parser.parse_args()))
