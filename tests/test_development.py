import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

from tools import develop
from tools import build_release


class DevelopmentTests(unittest.TestCase):
    def test_release_archives_distinguish_blender_intervals_with_shared_python(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def fake_build(**kwargs):
                archive = root / 'same-abi.zip'
                archive.write_text(kwargs['blender_min'])
                return archive
            with patch.object(build_release.build_addon, 'build', side_effect=fake_build):
                first = build_release.build('4.2', 'windows-x64', root, root)
                second = build_release.build('4.5', 'windows-x64', root, root)
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_text(), '4.2.0')
            self.assertEqual(second.read_text(), '4.5.0')

    def test_sync_preserves_binaries_updates_code_and_removes_stale_owned_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            source = root / 'freemocap_blender_addon'
            source.mkdir(parents=True)
            (source / '__init__.py').write_text('version = 2')
            stage = Path(directory) / 'stage'
            package = stage / 'user/scripts/addons/freemocap_blender_addon'
            package.mkdir(parents=True)
            (package / 'removed.py').write_text('old')
            (package / '_dependencies').mkdir()
            binary = package / '_dependencies/pinned.dll'
            binary.write_bytes(b'never rewrite while Blender is running')
            timestamp = binary.stat().st_mtime_ns
            state = root / 'state.json'
            state.write_text(json.dumps(dict(stage=str(stage), source_files=['removed.py'])))
            (stage / 'development-owner.json').write_text(json.dumps(dict(repository=str(root), state=str(state.resolve()))))
            with patch.object(develop, 'ROOT', root):
                develop.sync(state)
                develop.sync(state)
            self.assertEqual((package / '__init__.py').read_text(), 'version = 2')
            self.assertFalse((package / 'removed.py').exists())
            self.assertEqual(binary.stat().st_mtime_ns, timestamp)

    def test_sync_refuses_unowned_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / 'state.json'
            state.write_text(json.dumps(dict(stage=str(root))))
            (root / 'development-owner.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'ownership'):
                develop.sync(state)

    def test_background_arguments_reach_installed_api(self):
        spec = importlib.util.spec_from_file_location('export_runner', develop.ROOT / 'tools/blender_export.py')
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        calls = []
        api = types.SimpleNamespace(export_recording=lambda **kwargs: calls.append(kwargs))
        addon = types.SimpleNamespace(__freemocap_export_api__=True)
        bpy = types.SimpleNamespace(context=types.SimpleNamespace(preferences=types.SimpleNamespace(addons={'installed': True})))
        with patch.dict('sys.modules', bpy=bpy), patch.object(runner.importlib, 'import_module', side_effect=[addon, api]):
            runner.main(['installed', 'input.parquet', 'output.blend', '--route', 'parquet_constraints',
                         '--trajectory-channel', 'MAPPED_KEYPOINTS_3D', '--run-id', '3', '--sensor-group', 'camera_group:a'])
        self.assertEqual(calls, [dict(recording_path='input.parquet', blend_file_path='output.blend',
            route='parquet_constraints', trajectory_channel='MAPPED_KEYPOINTS_3D', run_id=3, sensor_group='camera_group:a', config=None)])
