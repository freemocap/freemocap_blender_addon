"""Prepare an isolated, reloadable VS Code workspace; no global Python installs.

python -B -m tools.develop prepare --blender /path/to/blender
JacquesLucke's build task subsequently runs `sync --state ...` before reload.
The development container uses the legacy bundle even on modern Blender: its
private binaries survive the editor's disable/re-enable cycle. Release Extensions
still use unmodified wheels and Blender's own dependency management.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

from tools import build_addon, run_tests, test_blender_package

ROOT = Path(__file__).resolve().parents[1]
TASK = 'FreeMoCap: sync Blender development code'


def source_files(root):
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if (path.is_file() and not any(p.startswith('.') or p in ('__pycache__', '_dependencies', 'wheels', '_host_tools') for p in relative.parts)
                and path.name not in build_addon.EXCLUDED
                and path.name not in ('build-info.json', 'dependency-lock.json', '_legacy_dependencies.json', 'blender_manifest.toml')
                and path.suffix not in ('.pyc', '.blend1')):
            yield relative, path


def sync(state_path):
    state_path = Path(state_path).resolve()
    state = json.loads(state_path.read_text(encoding='utf-8'))
    stage = Path(state['stage']).resolve()
    if stage == ROOT or ROOT.is_relative_to(stage) or stage.is_relative_to(ROOT / build_addon.PACKAGE):
        raise ValueError('Development stage must not contain or replace source')
    owner = json.loads((stage / 'development-owner.json').read_text(encoding='utf-8'))
    if owner != dict(repository=str(ROOT), state=str(state_path)):
        raise ValueError('Development directory ownership does not match this checkout')
    package = stage / 'user/scripts/addons' / build_addon.PACKAGE
    if not package.resolve().is_relative_to(stage):
        raise ValueError('Development package escapes its managed directory')
    current = dict(source_files(ROOT / build_addon.PACKAGE))
    old = [Path(p) for p in state.get('source_files', [])]
    for relative in list(current) + old:
        target = package / relative
        if relative.is_absolute() or '..' in relative.parts or not target.resolve().is_relative_to(package.resolve()):
            raise ValueError('Unsafe development source path')
    for relative, source in current.items():
        target = package / relative
        content = source.read_bytes()
        if not target.is_file() or target.read_bytes() != content:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    for relative in old:
        if relative not in current:
            (package / relative).unlink(missing_ok=True)
    state['source_files'] = [p.as_posix() for p in current]
    from tools.build_identity import write_identity
    runtime = json.loads((package / '_legacy_dependencies.json').read_text())['runtime']
    platform = next(name for name, target in build_addon.PLATFORMS.items() if list(target[:2]) == runtime[:2])
    write_identity(root=ROOT, package=package, version=build_addon.package_version(),
                   kind='development', python=runtime[2], platform=platform)
    state_path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')
    return package


def prepare(blender, download=False):
    blender = Path(blender).resolve()
    if not blender.is_file():
        raise ValueError('Blender executable does not exist: ' + str(blender))
    artifacts = ROOT / '.test-artifacts/development'
    artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='fmc-probe-') as temporary:
        runtime = run_tests.probe(blender, Path(temporary))
    platform, _ = run_tests.target(runtime)
    cache = ROOT / '.test-artifacts/wheels'
    try:
        entries = build_addon.wheel_set(cache, runtime['python'], platform, download)
    except FileNotFoundError as exc:
        raise RuntimeError('No complete wheel cache for this Blender. Run prepare again with --download '
                           'to explicitly acquire the pinned build dependencies.') from exc
    # Different runtimes or dependency pins get a fresh stage, so live DLLs are
    # never replaced. Source-only reloads reuse the original dependency files.
    identity = json.dumps([str(ROOT), str(blender), runtime, entries], sort_keys=True)
    token = hashlib.sha256(identity.encode()).hexdigest()[:12]
    stage = Path(tempfile.gettempdir()) / ('fmc-dev-' + token)
    state_path = (artifacts / (token + '.json')).resolve()
    owner = dict(repository=str(ROOT), state=str(state_path))
    marker = stage / 'development-owner.json'
    if stage.exists():
        if not marker.is_file() or json.loads(marker.read_text()) != owner:
            raise ValueError('Refusing to overwrite an unowned development directory: ' + str(stage))
        if not state_path.is_file():
            raise ValueError('Incomplete development setup; use a fresh temporary directory')
    else:
        archive = build_addon.build(kind='legacy', python=runtime['python'], platform=platform,
                                    cache=cache, output=artifacts / token)
        stage.mkdir()
        marker.write_text(json.dumps(owner), encoding='utf-8')
        scripts = stage / 'user/scripts/addons'
        build_addon.expand_wheel(archive, scripts)
        state_path.write_text(json.dumps(dict(stage=str(stage), blender=str(blender), runtime=runtime,
                                               source_files=[])), encoding='utf-8')
    package = sync(state_path)
    environment = test_blender_package.isolated_environment(stage / 'user')
    overrides = {k: v for k, v in environment.items() if k.startswith('BLENDER_USER_')}
    overrides.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHONPATH='', PYTHONHOME='')
    version = '.'.join(map(str, runtime['blender']))
    workspace = artifacts / ('Blender-' + version + '.code-workspace')
    workspace.write_text(json.dumps(dict(
        folders=[dict(path=str(ROOT))],
        settings={
            'blender.executables': [dict(path=str(blender), name='FreeMoCap ' + version, isDefault=True)],
            'blender.addonFolders': [str(ROOT)],
            'blender.addon.sourceDirectory': str(ROOT / build_addon.PACKAGE),
            'blender.addon.loadDirectory': str(package),
            'blender.addon.moduleName': build_addon.PACKAGE,
            'blender.addon.buildTaskName': TASK,
            'blender.addon.reloadOnSave': False,
            'blender.environmentVariables': overrides,
        },
        tasks=dict(version='2.0.0', tasks=[dict(label=TASK, type='process', command=sys.executable,
            args=['-B', '-m', 'tools.develop', 'sync', '--state', str(state_path)],
            options=dict(cwd=str(ROOT)), problemMatcher=[])]),
    ), indent=2) + '\n', encoding='utf-8')
    return dict(workspace=str(workspace), state=str(state_path), package=str(package),
                stage=str(stage), runtime=runtime)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    setup = sub.add_parser('prepare')
    setup.add_argument('--blender', type=Path, required=True)
    setup.add_argument('--download', action='store_true', help='Explicitly acquire pinned wheels if needed')
    update = sub.add_parser('sync')
    update.add_argument('--state', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'prepare':
        print(json.dumps(prepare(args.blender, args.download), indent=2))
    else:
        print('Development source refreshed: ' + str(sync(args.state)))


if __name__ == '__main__':
    main()
