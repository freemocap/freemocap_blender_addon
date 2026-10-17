import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from tools.package_catalog import catalog


class PackageCatalogTests(unittest.TestCase):
    def test_local_and_release_catalog_use_actual_archive_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory)/'freemocap-extension-blender5.2-py3.13-windows-x64.zip'
            identity = dict(package_format='extension', python='3.13', platform='windows-x64',
                            source_sha256='a'*64, version='2026.4.1041', source_commit='commit')
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr('build-info.json', json.dumps(identity))
            local = catalog(directory)['packages'][0]
            self.assertEqual(local['sha256'], hashlib.sha256(archive.read_bytes()).hexdigest())
            self.assertEqual(local['path'], archive.name)
            self.assertEqual(local['source_sha256'], identity['source_sha256'])
            remote = catalog(directory, 'https://example.invalid/release')['packages'][0]
            self.assertEqual(remote['url'], 'https://example.invalid/release/' + archive.name)
            self.assertNotIn('path', remote)
            with self.assertRaises(ValueError):
                catalog(directory, 'http://example.invalid')
            with self.assertRaisesRegex(ValueError, 'exact clean CI commit'):
                catalog(directory, 'https://example.invalid', commit='other')
            identity['source_dirty'] = False
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr('build-info.json', json.dumps(identity))
            self.assertEqual(catalog(directory, 'https://example.invalid', commit='commit')['source_commit'], 'commit')
