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
                        root = Path(temp)
                        recording = root / 'recording'
                        recording.mkdir()
                        source = recording
                        if file_input:
                            source = recording / 'recording_data.parquet'
                            source.write_bytes(b'test input')
                        output = root / 'custom.blend'
                        exporter = Mock()
                        scene = {'root': object(), 'rig': object()}
                        modules = {
                            'bpy': SimpleNamespace(ops=SimpleNamespace(wm=SimpleNamespace(
                                save_as_mainfile=lambda filepath: Path(filepath).write_bytes(b'blend')))),
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
