"""Offline packaging contracts; run with python -B -m unittest discover -s tests -p test_dependency_packaging.py."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_file('builder', ROOT / 'tools/build_addon.py')
legacy = load_file('legacy', ROOT / 'tools/legacy_dependencies.py')
dependencies = load_file('dependencies', ROOT / 'freemocap_blender_addon/utilities/dependencies.py')


class PackagingTests(unittest.TestCase):
    def test_binary_selection_rejects_wrong_abi_platform_and_free_threading(self):
        self.assertTrue(builder.matches('pyarrow-25.0.1-cp313-cp313-win_amd64.whl', '3.13', 'windows-x64'))
        for filename in ('pyarrow-25.0.1-cp312-cp312-win_amd64.whl',
                         'pyarrow-25.0.1-cp313-cp313t-win_amd64.whl',
                         'pyarrow-25.0.1-cp313-cp313-macosx_12_0_arm64.whl', 'bad.whl'):
            self.assertFalse(builder.matches(filename, '3.13', 'windows-x64'))

    def test_wheel_extraction_rejects_traversal_and_schemes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('../escape', '/absolute', 'C:/absolute', 'a\\escape', 'x.data/scripts/run'):
                with self.subTest(name=name):
                    wheel = root / 'unsafe.whl'
                    with zipfile.ZipFile(wheel, 'w') as archive:
                        entry = zipfile.ZipInfo('placeholder')
                        entry.filename = name  # Preserve deliberately invalid separators on Windows.
                        archive.writestr(entry, 'bad')
                    with self.assertRaises(ValueError):
                        builder.expand_wheel(wheel, root / 'expanded')

    def test_offline_lock_rejects_tampered_wheel(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entries = []
            for name, version in builder.requirements('3.13').items():
                filename = '{}-{}-py3-none-any.whl'.format(name, version)
                (root / filename).write_bytes(b'original')
                entries.append(dict(name=name, version=version, filename=filename,
                                    sha256=hashlib.sha256(b'original').hexdigest()))
            (root / '3.13-windows-x64.json').write_text(json.dumps(entries))
            builder.wheel_set(root, '3.13', 'windows-x64', False)
            (root / entries[0]['filename']).write_bytes(b'tampered')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                builder.wheel_set(root, '3.13', 'windows-x64', False)

    def test_extension_requires_explicit_compatible_interval(self):
        for kwargs in (dict(python='3.9'), dict(python='3.13'),
                       dict(python='3.13', blender_min='4.1.0', blender_max='4.2.0')):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                builder.build(kind='extension', platform='windows-x64', cache=None, output=None, **kwargs)

    def test_archive_separation_and_repeatability(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wheel = root / 'sample-1-py3-none-any.whl'
            with zipfile.ZipFile(wheel, 'w') as archive:
                archive.writestr('sample/__init__.py', '')
            entry = dict(filename=wheel.name)
            with patch.object(builder, 'wheel_set', return_value=[entry]):
                args = dict(python='3.13', platform='windows-x64', cache=root, output=root,
                            blender_min='5.2.0', blender_max='5.3.0')
                extension = builder.build(kind='extension', **args)
                digest = hashlib.sha256(extension.read_bytes()).digest()
                self.assertEqual(digest, hashlib.sha256(builder.build(kind='extension', **args).read_bytes()).digest())
                with zipfile.ZipFile(extension) as archive:
                    names = archive.namelist()
                    self.assertIn('blender_manifest.toml', names)
                    self.assertIn('wheels/' + wheel.name, names)
                    self.assertFalse(any(name.endswith(tuple(builder.EXCLUDED)) for name in names))
                    self.assertNotIn('bl_info =', archive.read('__init__.py').decode())
                    identity = json.loads(archive.read('build-info.json'))
                    self.assertEqual(identity['version'], builder.package_version())
                    self.assertEqual(identity['export_api_version'], 1)
                    self.assertEqual(identity['dependency_lock_sha256'], hashlib.sha256(archive.read('dependency-lock.json')).hexdigest())
                    archive.extractall(root / 'identity-check')
                    from tools.build_identity import identity_module
                    checker = identity_module(ROOT)
                    self.assertEqual(checker.read_identity(root / 'identity-check'), identity)
                    (root / 'identity-check/export_api.py').write_text('# local edit')
                    with self.assertRaisesRegex(ValueError, 'differ'):
                        checker.read_identity(root / 'identity-check')
                addon = builder.build(kind='legacy', **args)
                with zipfile.ZipFile(addon) as archive:
                    names = archive.namelist()
                    self.assertIn('freemocap_blender_addon/_dependencies/sample/__init__.py', names)
                    self.assertIn('freemocap_blender_addon/utilities/legacy_dependencies.py', names)
                    self.assertNotIn('blender_manifest.toml', names)
                    legacy_identity = json.loads(archive.read('freemocap_blender_addon/build-info.json'))
                    self.assertEqual(legacy_identity['source_sha256'], identity['source_sha256'])
                    self.assertEqual(legacy_identity['source_sha256'], checker.source_hash(ROOT / builder.PACKAGE))

    def test_source_parses_as_python39_and_uses_relative_imports(self):
        for path in (ROOT / builder.PACKAGE).rglob('*.py'):
            with self.subTest(path=path):
                tree = ast.parse(path.read_text(encoding='utf-8'), feature_version=(3, 9))
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        self.assertFalse((node.module or '').startswith(builder.PACKAGE))


class DependencyFailures(unittest.TestCase):
    def test_missing_dependency_is_distinct_from_incompatible_binary(self):
        missing = ModuleNotFoundError("No module named 'pyarrow'", name='pyarrow')
        with patch.object(dependencies.importlib, 'import_module', side_effect=missing):
            with self.assertRaisesRegex(dependencies.DependencyUnavailable, 'tools.develop prepare') as caught:
                dependencies.require_module('pyarrow.parquet')
            self.assertNotIn('binary compatibility', str(caught.exception))
        with patch.object(dependencies.importlib, 'import_module', side_effect=ImportError('DLL load failed')):
            with self.assertRaisesRegex(dependencies.DependencyUnavailable, 'binary compatibility'):
                dependencies.require_module('pyarrow.parquet')

    def test_missing_module_is_actionable_without_installing(self):
        with patch.object(dependencies.importlib, 'import_module', side_effect=ImportError('missing')):
            with self.assertRaisesRegex(dependencies.DependencyUnavailable, 'No packages were downloaded'):
                dependencies.require_module('pyarrow')
        with self.assertRaises(ValueError):
            dependencies.require_module('arbitrary_package')

    def test_legacy_rejects_wrong_runtime_before_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_legacy_dependencies.json').write_text(json.dumps(dict(runtime=['wrong'])))
            with self.assertRaisesRegex(RuntimeError, 'targets'):
                legacy.load_module('pyarrow', root)

    def test_legacy_preserves_foreign_module_and_restores_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            machine = legacy.platform.machine().lower()
            machine = {'amd64': 'x86_64', 'aarch64': 'arm64'}.get(machine, machine)
            runtime = [legacy.platform.system(), machine, '{}.{}'.format(*sys.version_info[:2])]
            (root / '_legacy_dependencies.json').write_text(json.dumps(dict(runtime=runtime)))
            foreign = types.ModuleType('pyarrow')
            foreign.__file__ = str(root / 'foreign/__init__.py')
            before = list(sys.path)
            with patch.dict(sys.modules, pyarrow=foreign):
                with self.assertRaisesRegex(RuntimeError, 'another package'):
                    legacy.load_module('pyarrow', root)
                self.assertIs(sys.modules['pyarrow'], foreign)
            with patch.object(legacy.importlib, 'import_module', side_effect=ImportError('broken')):
                with self.assertRaises(ImportError):
                    legacy.load_module('missing_package', root)
            self.assertEqual(before, sys.path)


if __name__ == '__main__':
    unittest.main()
