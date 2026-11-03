"""Public API destination contract without requiring a Blender installation."""
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from freemocap_blender_addon.export_api import export_recording


class ExportDestinationTests(unittest.TestCase):
    def test_model_exports_belong_to_recording_not_custom_blend_destination(self):
        for route in ('parquet_segments', 'parquet_constraints'):
            for file_input in (False, True):
                for formats in ([], ['fbx'], ['bvh'], ['fbx', 'bvh']):
                    with self.subTest(route=route, file_input=file_input, formats=formats), TemporaryDirectory() as temp:
                        root = Path(temp).resolve()
                        recording = root / 'recording'
                        recording.mkdir()
                        source = recording
                        if file_input:
                            source = recording / 'recording_data.parquet'
                            source.write_bytes(b'test input')
                        output = root / 'custom.blend'
                        exporter = Mock(return_value=())
                        scene = {'root': object(), 'rig': object()}
                        modules = {
                            'bpy': SimpleNamespace(ops=SimpleNamespace(wm=SimpleNamespace(
                                save_as_mainfile=lambda filepath: (Path(filepath).write_bytes(b'blend'), {'FINISHED'})[1]))),
                            'freemocap_blender_addon.core_functions.parquet_import': SimpleNamespace(load_parquet=Mock(return_value=scene)),
                            'freemocap_blender_addon.core_functions.animation_cleanup': SimpleNamespace(apply_cleanup=Mock()),
                            'freemocap_blender_addon.core_functions.export_3d_model.export_3d_model': SimpleNamespace(export_3d_model=exporter),
                        }
                        with patch.dict('sys.modules', modules):
                            self.assertEqual(export_recording(recording_path=source, blend_file_path=output,
                                route=route, config={'export_3d_model': {'formats': formats}}), str(output.resolve()))
                        if formats:
                            exporter.assert_called_once_with(scene['root'], scene['rig'], formats=formats,
                                destination_folder=str(recording / 'exports'), add_subfolder=True)
                        else:
                            exporter.assert_not_called()
                        self.assertTrue(output.is_file())

    def test_result_reports_only_producer_files_and_preserves_string_entry_point(self):
        from freemocap_blender_addon.export_api import export_recording_result
        with TemporaryDirectory() as temp:
            root = Path(temp).resolve(); recording = root / 'recording'; recording.mkdir()
            output = root / 'scene.blend'
            stale = recording / 'stale.fbx'; stale.write_bytes(b'old')
            files = [recording / name for name in ('subject.fbx', 'subject.bvh', 'subject.bvh.metadata.json')]
            def produce(*args, **kwargs):
                for file in files: file.write_bytes(b'new export')
                return tuple(str(file) for file in files)
            modules = {
                'bpy': SimpleNamespace(ops=SimpleNamespace(wm=SimpleNamespace(
                    save_as_mainfile=lambda filepath: (Path(filepath).write_bytes(b'blend'), {'FINISHED'})[1]))),
                'freemocap_blender_addon.core_functions.parquet_import': SimpleNamespace(
                    load_parquet=lambda *args, **kwargs: {'root': object(), 'rig': object()}),
                'freemocap_blender_addon.core_functions.animation_cleanup': SimpleNamespace(apply_cleanup=Mock()),
                'freemocap_blender_addon.core_functions.export_3d_model.export_3d_model': SimpleNamespace(export_3d_model=produce),
            }
            with patch.dict('sys.modules', modules):
                result = export_recording_result(recording_path=recording, blend_file_path=output,
                    route='parquet_segments', config={'export_3d_model': {'formats': ['fbx','bvh']}})
            self.assertEqual(result, {'output':str(output),'files':[*map(str,files),str(output)]})
            self.assertNotIn(str(stale),result['files'])
            self.assertTrue(all(Path(file).is_file() for file in result['files']))

    def test_cancelled_save_does_not_report_stale_blend(self):
        with TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            output = root / 'old.blend'
            output.write_bytes(b'old blend')
            report = Mock()
            modules = {
                'bpy': SimpleNamespace(ops=SimpleNamespace(wm=SimpleNamespace(
                    save_as_mainfile=lambda **kwargs: {'CANCELLED'}))),
                'freemocap_blender_addon.core_functions.parquet_import': SimpleNamespace(
                    load_parquet=lambda *args, **kwargs: {'root': object(), 'rig': object()}),
                'freemocap_blender_addon.core_functions.animation_cleanup': SimpleNamespace(apply_cleanup=Mock()),
            }
            with patch.dict('sys.modules', modules), self.assertRaisesRegex(RuntimeError, 'did not finish saving'):
                export_recording(recording_path=root, blend_file_path=output,
                    route='parquet_segments', config={'export_3d_model': {'formats': []}},
                    artifact_report=report)
            report.assert_not_called()
            self.assertEqual(output.read_bytes(), b'old blend')
