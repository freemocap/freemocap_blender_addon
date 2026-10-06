"""One-command local test suite. Blender Launcher owns Blender downloads/updates.

Run from the repository: python -B -m tools.run_tests
Use --launcher-library for a custom Launcher library or repeated --blender paths
for CI/explicit builds. --download-wheels allows build-time dependency acquisition;
without it every build uses the existing verified wheel cache, with no downloads.
"""
import argparse
import configparser
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

from tools import build_addon, test_blender_package, reference_data

ROOT = Path(__file__).resolve().parents[1]
CHANNELS = ('stable', 'daily', 'experimental', 'custom')


def launcher_library():
    local = os.environ.get('LOCALAPPDATA')
    if not local:
        raise ValueError('Use --launcher-library or --blender on this platform')
    directory = Path(local) / 'Blender Launcher'
    ini = directory / 'Blender Launcher.ini'
    if ini.is_file():
        config = configparser.ConfigParser(interpolation=None)
        config.read(ini, encoding='utf-8-sig')
        configured = config.get('General', 'library_folder', fallback='')
        if configured:
            # Qt INI files escape Windows path separators.
            directory = Path(configured.replace('\\\\', '\\'))
    return directory


def discover(library):
    candidates = []
    # Restrict discovery to Launcher build directories, not disks or user projects.
    for channel in CHANNELS:
        directory = Path(library) / channel
        if directory.is_dir():
            for name in ('blender.exe', 'blender'):
                candidates.extend(path.resolve() for path in directory.rglob(name) if path.is_file())
    return sorted(set(candidates))


def probe(blender, output):
    blender = Path(blender).resolve()
    output = Path(output).resolve()
    expression = (
        "import bpy,sys,platform,json; "
        "print('FREEMOCAP_RUNTIME ' + json.dumps(dict(blender=list(bpy.app.version), "
        "python='{}.{}'.format(*sys.version_info[:2]), system=platform.system(), machine=platform.machine())))"
    )
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([str(blender), '--background', '--factory-startup', '--python-exit-code', '1',
                             '--python-expr', expression],
                            cwd=output, env=test_blender_package.isolated_environment(output / 'user'),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    log = result.stdout.decode('utf-8', errors='replace')
    (output / 'probe.log').write_text(log, encoding='utf-8')
    if result.returncode:
        raise RuntimeError('Blender probe failed; see ' + str(output / 'probe.log'))
    lines = [line for line in log.splitlines() if line.startswith('FREEMOCAP_RUNTIME ')]
    if len(lines) != 1:
        raise RuntimeError('Blender did not report a unique runtime; see ' + str(output / 'probe.log'))
    return json.loads(lines[0].split(' ', 1)[1])


def target(runtime):
    version = tuple(runtime['blender'])
    if version < (3, 0, 0):
        raise ValueError('Blender older than 3.0 is outside the test target')
    machine = runtime['machine'].lower()
    machine = {'amd64': 'x86_64', 'aarch64': 'arm64'}.get(machine, machine)
    choices = {('Windows', 'x86_64'): 'windows-x64', ('Linux', 'x86_64'): 'linux-x64',
               ('Darwin', 'x86_64'): 'macos-x64', ('Darwin', 'arm64'): 'macos-arm64'}
    platform = choices.get((runtime['system'], machine))
    if platform is None:
        raise ValueError('No supported wheel target for this runtime: ' + repr(runtime))
    return platform, ['legacy', 'extension'] if version >= (4, 2, 0) else ['legacy']


def write_reports(output, results):
    (output / 'summary.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    suite = ET.Element('testsuite', name='freemocap_blender_addon', tests=str(len(results)),
                       failures=str(sum(r['status'] == 'failed' for r in results)))
    for result in results:
        case = ET.SubElement(suite, 'testcase', name=result['name'], time=str(result['seconds']))
        if result['status'] == 'failed':
            ET.SubElement(case, 'failure', message=result['error']).text = result['error']
        ET.SubElement(case, 'system-out').text = json.dumps(result, indent=2)
    ET.ElementTree(suite).write(output / 'junit.xml', encoding='utf-8', xml_declaration=True)


def main(arguments=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--launcher-library', type=Path)
    parser.add_argument('--blender', type=Path, action='append', default=[])
    parser.add_argument('--unit-only', action='store_true')
    parser.add_argument('--download-wheels', action='store_true')
    parser.add_argument('--dataset', choices=('all', 'none', 'test_data', 'sample_data'), default='all')
    parser.add_argument('--prepared-root', type=Path, default=Path(os.environ.get(
        'FREEMOCAP_PROVENANCE_PREPARED_ROOT', Path.home() / 'freemocap_data/testing/prepared')))
    args = parser.parse_args(arguments)
    artifacts = ROOT / '.test-artifacts'
    artifacts.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='suite-', dir=artifacts))
    results = []

    def check(name, function, **metadata):
        started = time.monotonic()
        record = dict(name=name, **metadata)
        try:
            details = function()
            if details is not None:
                record['details'] = details
            record['status'] = 'passed'
        except Exception as exc:
            record.update(status='failed', error=str(exc))
        record['seconds'] = round(time.monotonic() - started, 3)
        results.append(record)
        write_reports(output, results)
        print('{}: {}'.format(record['status'].upper(), name), flush=True)
        if record['status'] == 'failed':
            print(record['error'], flush=True)

    def units():
        with (output / 'unit.log').open('w', encoding='utf-8') as log:
            subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'],
                           cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=180)
    check('offline unit suite', units)
    if not args.unit_only:
        references = []
        datasets = list(reference_data.DATASETS) if args.dataset == 'all' else ([] if args.dataset == 'none' else [args.dataset])
        for dataset in datasets:
            check('reference snapshot ' + dataset, lambda: references.append(
                reference_data.snapshot(args.prepared_root, dataset, output / 'references')))
        manifest = output / 'references.json'
        manifest.write_text(json.dumps(references, indent=2), encoding='utf-8')
        builds = []
        def discovery():
            builds.extend(sorted(set(p.resolve() for p in args.blender)) if args.blender else
                          discover(args.launcher_library or launcher_library()))
            if not builds:
                raise RuntimeError('No Blender builds found. Install one in Blender Launcher or use --blender PATH.')
        check('Blender discovery', discovery)
        for index, blender in enumerate(builds):
            folder = output / ('build-{}'.format(index))
            runtime = {}
            def inspect():
                runtime.update(probe(blender, folder))
                target(runtime)
            check('probe ' + str(blender), inspect, executable=str(blender))
            if results[-1]['status'] == 'failed':
                continue
            platform, kinds = target(runtime)
            for kind in kinds:
                def package_test():
                    major, minor, patch = runtime['blender']
                    archive = build_addon.build(kind=kind, python=runtime['python'], platform=platform,
                                                cache=artifacts / 'wheels', output=folder / 'packages',
                                                download=args.download_wheels,
                                                blender_min='{}.{}.0'.format(major, minor),
                                                blender_max='{}.{}.0'.format(major, minor + 1))
                    test_blender_package.run(blender, kind, archive, output=folder / kind, references=manifest)
                    return json.loads((folder / kind / 'report.json').read_text(encoding='utf-8'))
                check('{} {}'.format(blender.parent.name, kind), package_test,
                      executable=str(blender), runtime=dict(runtime), kind=kind, logs=str(folder / kind))
        if references:
            check('shared reference integrity after tests', lambda: reference_data.verify_unchanged(references))
    print('Suite reports: ' + str(output), flush=True)
    return int(any(r['status'] == 'failed' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
