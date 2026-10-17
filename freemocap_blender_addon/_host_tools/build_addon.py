"""Build offline runtime packages from pinned, hash-verified PyPI wheels.

No pip, environment installation, Git operations or publishing. --download is
explicit build-time network access. Without it, a verified local wheel lock is
required. Archives contain a deterministic file order and timestamp.
"""
import importlib.util
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "freemocap_blender_addon"
PLATFORMS = {
    "windows-x64": ("Windows", "x86_64", ("win_amd64",)),
    "linux-x64": ("Linux", "x86_64", ("manylinux_2_28_x86_64", "manylinux_2_17_x86_64")),
    "macos-x64": ("Darwin", "x86_64", ("macosx_12_0_x86_64",)),
    "macos-arm64": ("Darwin", "arm64", ("macosx_12_0_arm64",)),
}
EXCLUDED = {"install_dependencies.py", "git_source_manager.py", "legacy_dependencies.py"}


def requirements(python):
    return {"pyarrow": "18.1.0" if python == "3.9" else "25.0.1", "tomli": "2.2.1"}


def matches(filename, python, platform):
    if not filename.endswith(".whl"):
        return False
    parts = filename[:-4].rsplit("-", 3)
    if len(parts) != 4:
        return False
    _, interpreter, abi, wheel_platform = parts
    if interpreter == "py3" and abi == "none" and wheel_platform == "any":
        return True
    cp = "cp" + python.replace(".", "")
    return interpreter == cp and abi == cp and bool(set(wheel_platform.split(".")) & set(PLATFORMS[platform][2]))


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def wheel_set(cache, python, platform, download):
    cache.mkdir(parents=True, exist_ok=True)
    lock_path = cache / ("{}-{}.json".format(python, platform))
    pins = requirements(python)
    if download:
        entries = []
        for name, version in pins.items():
            metadata = fetch_json("https://pypi.org/pypi/{}/{}/json".format(name, version))
            # These pins have no mandatory external dependencies. Fail if that changes;
            # do not ship an incomplete environment or invent dependency resolution.
            mandatory = [r for r in metadata['info'].get('requires_dist') or [] if 'extra ==' not in r and 'extra==' not in r]
            if mandatory:
                raise ValueError("Review and pin transitive dependencies: {}".format(mandatory))
            candidates = [item for item in metadata["urls"] if not item.get("yanked") and matches(item["filename"], python, platform)]
            if not candidates:
                raise ValueError("No wheel for {} {} on Python {} / {}".format(name, version, python, platform))
            item = sorted(candidates, key=lambda x: x["filename"])[0]
            entry = dict(name=name, version=version, filename=item["filename"], sha256=item["digests"]["sha256"], url=item["url"])
            destination = cache / entry["filename"]
            if not destination.is_file() or hashlib.sha256(destination.read_bytes()).hexdigest() != entry["sha256"]:
                with urllib.request.urlopen(entry["url"], timeout=120) as response:
                    data = response.read()
                if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                    raise ValueError("Wheel hash mismatch")
                destination.write_bytes(data)
            entries.append(entry)
        lock_path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    entries = json.loads(lock_path.read_text(encoding="utf-8"))
    if len(entries) != len(pins) or {e["name"]: e["version"] for e in entries} != pins:
        raise ValueError("Wheel lock does not match dependency pins")
    for entry in entries:
        name = entry["filename"]
        if '/' in name or '\\' in name or ':' in name or not matches(name, python, platform):
            raise ValueError("Invalid or incompatible wheel filename")
        if hashlib.sha256((cache / name).read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError("Wheel hash mismatch: " + name)
    return entries


def expand_wheel(wheel, target):
    with zipfile.ZipFile(wheel) as archive:
        for item in archive.infolist():
            path = PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or '\\' in item.orig_filename or ':' in item.filename:
                raise ValueError("Unsafe wheel entry: " + item.filename)
            if any(part.endswith('.data') for part in path.parts):
                raise ValueError("Wheel installation schemes require explicit support")
            if item.is_dir():
                continue
            destination = target.joinpath(*path.parts)
            if destination.exists():
                raise ValueError("Wheel file collision: " + item.filename)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(item))


def extension_init(text):
    tree = ast.parse(text)
    lines = text.splitlines(keepends=True)
    for node in reversed(tree.body):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'bl_info' for t in node.targets):
            del lines[node.lineno - 1:node.end_lineno]
    return ''.join(lines)


def package_version():
    # Read metadata without importing bpy or executing the package.
    tree = ast.parse((ROOT / PACKAGE / '__init__.py').read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '__version__' for t in node.targets):
            parts = ast.literal_eval(node.value).removeprefix('v').split('.')
            if len(parts) != 3 or not all(p.isdecimal() for p in parts):
                raise ValueError('A stable three-part package version is required')
            return '.'.join(str(int(p)) for p in parts)
    raise ValueError('Missing package version')


def build(*, kind, python, platform, cache, output, download=False, blender_min=None, blender_max=None, provenance=None):
    if kind not in ('extension', 'legacy') or platform not in PLATFORMS:
        raise ValueError('Unsupported package format or platform')
    if python not in ('3.9', '3.10', '3.11', '3.12', '3.13', '3.14'):
        raise ValueError("Unsupported Python target")
    if kind == 'extension' and python in ('3.9', '3.10'):
        raise ValueError("Extensions require Blender 4.2+, with Python 3.11 or newer")
    if kind == 'extension' and (not blender_min or not blender_max):
        raise ValueError("Specify the tested Blender version interval for this Python ABI")
    if kind == 'extension':
        lower, upper = tuple(map(int, blender_min.split('.'))), tuple(map(int, blender_max.split('.')))
        if len(lower) != 3 or len(upper) != 3 or lower < (4, 2, 0) or upper <= lower:
            raise ValueError("Invalid Blender version interval")
    entries = wheel_set(cache, python, platform, download)
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='freemocap-build-') as temporary:
        staging = Path(temporary)
        package = staging / PACKAGE if kind == 'legacy' else staging
        package.mkdir(exist_ok=True)
        for path in sorted((ROOT / PACKAGE).rglob('*')):
            relative = path.relative_to(ROOT / PACKAGE)
            if not path.is_file() or any(p.startswith('.') or p in ('__pycache__', '_host_tools') for p in relative.parts):
                continue
            if path.name in EXCLUDED or path.name == 'build-info.json' or path.suffix in ('.pyc', '.blend1'):
                continue
            destination = package / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
        shutil.copyfile(Path(__file__).with_name('LICENSE'), package / 'LICENSE')
        (package / 'dependency-lock.json').write_text(json.dumps(entries, indent=2)+'\n', encoding='utf-8')
        if kind == 'extension':
            init = package / '__init__.py'
            init.write_text(extension_init(init.read_text(encoding='utf-8')), encoding='utf-8')
            (package / 'wheels').mkdir()
            for entry in entries:
                shutil.copyfile(cache / entry['filename'], package / 'wheels' / entry['filename'])
            manifest = '\n'.join([
                'schema_version = "1.0.0"', 'id = "freemocap_blender_addon"',
                'version = ' + json.dumps(package_version()), 'name = "FreeMoCap"',
                'tagline = "Load and animate motion capture recordings"',
                'maintainer = "FreeMoCap <info@freemocap.org>"', 'type = "add-on"',
                'blender_version_min = ' + json.dumps(blender_min),
                'blender_version_max = ' + json.dumps(blender_max),
                # Preserve the actual repository license; marketplace approval is separate.
                'license = ["SPDX:AGPL-3.0-only"]',
                'platforms = ' + json.dumps([platform]),
                'wheels = ' + json.dumps(['./wheels/'+e['filename'] for e in entries]),
                '[permissions]', 'files = "Read motion capture recordings and save animations"', '',
            ])
            (package / 'blender_manifest.toml').write_text(manifest, encoding='utf-8')
        else:
            shutil.copyfile(Path(__file__).with_name('legacy_dependencies.py'), package / 'utilities/legacy_dependencies.py')
            for entry in entries:
                expand_wheel(cache / entry['filename'], package / '_dependencies')
            runtime = list(PLATFORMS[platform][:2]) + [python]
            (package / '_legacy_dependencies.json').write_text(json.dumps(dict(runtime=runtime)), encoding='utf-8')
        spec = importlib.util.spec_from_file_location('fmc_host_identity', Path(__file__).with_name('build_identity.py'))
        identity_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(identity_module)
        write_identity = identity_module.write_identity
        write_identity(root=ROOT, package=package, version=package_version(), kind=kind,
                       python=python, platform=platform, provenance=provenance)
        destination = output / ('freemocap-{}-py{}-{}.zip'.format(kind, python, platform))
        with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(staging.rglob('*')):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(staging).as_posix(), (2026, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o644 << 16
                    archive.writestr(info, path.read_bytes())
        return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', choices=('extension', 'legacy'), required=True)
    parser.add_argument('--python', required=True)
    parser.add_argument('--platform', choices=PLATFORMS, required=True)
    parser.add_argument('--cache', type=Path, default=ROOT / '.test-artifacts/wheels')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--blender-min')
    parser.add_argument('--blender-max')
    print(build(**vars(parser.parse_args())))
