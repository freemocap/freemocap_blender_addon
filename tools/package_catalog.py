"""Describe built packages for FreeMoCap's automatic Blender setup."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


def catalog(directory, base_url=None, commit=None):
    packages = []
    for archive in sorted(Path(directory).glob('freemocap-*-blender*-py*.zip')):
        match = re.fullmatch(r'freemocap-(extension|legacy)-blender([0-9.]+)-py([0-9.]+)-(.+)\.zip', archive.name)
        if not match:
            raise ValueError('Unrecognized package name: ' + archive.name)
        kind, blender, python, platform = match.groups()
        with zipfile.ZipFile(archive) as bundle:
            prefix = '' if kind == 'extension' else 'freemocap_blender_addon/'
            identity = json.loads(bundle.read(prefix + 'build-info.json'))
        if (identity['package_format'], identity['python'], identity['platform']) != (kind, python, platform):
            raise ValueError('Package name disagrees with build identity')
        if commit and (identity['source_commit'] != commit or identity.get('source_dirty') is not False):
            raise ValueError('Published packages must come from the exact clean CI commit')
        entry = dict(blender=blender, python=python, platform=platform,
                     source_sha256=identity['source_sha256'], version=identity['version'],
                     source_commit=identity['source_commit'], sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
        if base_url:
            if not base_url.startswith('https://'):
                raise ValueError('Published package URLs must use HTTPS')
            entry['url'] = base_url.rstrip('/') + '/' + archive.name
        else:
            entry['path'] = archive.name
        packages.append(entry)
    if not packages:
        raise ValueError('No built packages found')
    return dict(schema_version=1, source_commit=commit, packages=packages)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--base-url')
    parser.add_argument('--commit')
    args = parser.parse_args()
    destination = args.directory / 'package-catalog.json'
    destination.write_text(json.dumps(catalog(args.directory, args.base_url, args.commit), indent=2) + '\n', encoding='utf-8')
    print(destination)
