import gzip
import json
from pathlib import Path
import unittest


class PortableSkellyTests(unittest.TestCase):
    def test_asset_contains_rendered_geometry_and_binding_anchors(self):
        asset = Path(__file__).resolve().parents[1] / 'freemocap_blender_addon/assets/skelly_mesh.json.gz'
        with gzip.open(asset, 'rt', encoding='utf-8') as stream:
            data = json.load(stream)
        self.assertEqual(data['schema_version'], 1)
        self.assertEqual(len(data['vertices']), 10604)
        self.assertEqual(len(data['faces']), 20011)
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
