"""Exercise the actual Parquet artifact collector with Blender operators isolated."""
import importlib
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch


class Object:
    def __init__(self):
        self.children = []
        self.animation_data = None
        self.data = SimpleNamespace(copy=lambda: object())
        self.pose = SimpleNamespace(bones=[])
    def copy(self):
        return Object()
    def hide_get(self):
        return False
    def hide_set(self, value):
        pass
    def select_set(self, value):
        pass


class ArtifactInventoryTests(unittest.TestCase):
    def test_actual_bvh_collector_reports_only_segment_sidecar(self):
        for route in ('parquet_segments', 'parquet_constraints'):
            with self.subTest(route=route), TemporaryDirectory() as temp:
                rig = Object()
                root = SimpleNamespace(name='subject', get=lambda key: route if key == 'import_route' else None)
                scene = SimpleNamespace(frame_current=1, frame_start=1, frame_end=2, frame_set=Mock())
                def write_bvh(filepath, **kwargs):
                    Path(filepath).write_bytes(b'new bvh')
                    return {'FINISHED'}
                bpy = SimpleNamespace(
                    context=SimpleNamespace(scene=scene, selected_objects=[],
                        collection=SimpleNamespace(objects=SimpleNamespace(link=Mock())),
                        view_layer=SimpleNamespace(objects=SimpleNamespace(active=rig), update=Mock())),
                    ops=SimpleNamespace(object=SimpleNamespace(select_all=Mock()),
                        export_anim=SimpleNamespace(bvh=write_bvh)),
                    data=SimpleNamespace(objects=SimpleNamespace(remove=Mock()),
                        armatures=SimpleNamespace(remove=Mock()), actions=SimpleNamespace(remove=Mock())))
                name = 'freemocap_blender_addon.core_functions.export_3d_model.parquet_export'
                with patch.dict('sys.modules', {'bpy': bpy}):
                    module = importlib.import_module(name)
                    with patch.object(module, 'bpy', bpy), patch.object(module, 'get_fcurves_from_object_action', return_value=None):
                        files = module.export(root, rig, ['bvh'], temp, False, 'default', 'default', False, 'Y', 'X')
                expected = {str((Path(temp) / 'subject.bvh').resolve())}
                if route == 'parquet_segments':
                    expected.add(str((Path(temp) / 'subject.bvh.metadata.json').resolve()))
                    bpy.data.objects.remove.assert_called_once()
                self.assertEqual(set(files), expected)
                self.assertTrue(all(Path(file).stat().st_size for file in files))
                scene.frame_set.assert_called_once_with(1)
