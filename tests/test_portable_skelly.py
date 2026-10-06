import gzip
import json
from pathlib import Path
import unittest


class PortableSkellyTests(unittest.TestCase):
    def test_asset_contains_rendered_geometry_and_binding_anchors(self):
        asset = Path(__file__).resolve().parents[1] / 'freemocap_blender_addon/assets/skelly_mesh.json.gz'
        with gzip.open(asset, 'rt', encoding='utf-8') as stream:
            data = json.load(stream)
        self.assertEqual(data['schema_version'], 2)
        self.assertEqual(data['coordinate_system'], 'blender_x_right_y_forward_z_up')
        def anchor(name):
            return data['vertices'][data['groups'][name][0][0]]
        self.assertGreater(anchor('face_end')[1], anchor('face_origin')[1])
        self.assertLess(anchor('pelvis_left')[0], anchor('pelvis_right')[0])
        self.assertEqual(data['attachment_frames']['face']['roll_reference'], [0, 0, 1])
        self.assertEqual(len(data['vertices']), 10604)
        self.assertEqual(len(data['faces']), 20011)
        self.assertEqual([m['name'] for m in data['materials']], ['Base', 'Cavities', 'Sparkles'])
        self.assertEqual(len(data['face_materials']), len(data['faces']))
        self.assertEqual(set(data['face_materials']), {0, 1, 2})
        self.assertEqual(len(data['face_smooth']), len(data['faces']))
        self.assertEqual(len(data['groups']), 265)
        for group, weights in data['groups'].items():
            for index, weight in weights:
                self.assertTrue(0 <= index < len(data['vertices']), group)
                self.assertTrue(0 <= weight <= 1, group)
        for anchor in ('pelvis_origin', 'pelvis_left', 'pelvis_right',
                       'face_origin', 'face_end', 'upper_arm.L_origin', 'upper_arm.L_end'):
            self.assertTrue(data['groups'][anchor], anchor)
        for face in data['faces']:
            self.assertTrue(all(0 <= v < len(data['vertices']) for v in face))
