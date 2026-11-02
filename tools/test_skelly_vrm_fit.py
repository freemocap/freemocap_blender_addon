"""Presentation fitting regression using Forge's authored rest geometry."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from skellyforge.core.skeleton.skeleton_definition import SkeletonDefinition
from skellyforge.core.skeleton.pose.rest_pose import RestPose

from prepare_skelly_vrm import prepare


class AvatarFitTests(unittest.TestCase):
    def setUp(self):
        self.skeleton = SkeletonDefinition.from_default_yaml()
        self.rest = RestPose.from_default_yaml(skeleton=self.skeleton)
        artifact_directory = Path(__file__).resolve().parents[1] / '.test-artifacts/vrm'
        artifact_directory.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=artifact_directory)
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'artwork.json'
        # Model contract only: fitting must not mutate any supplied artwork.
        self.artwork = dict(coordinateSystem='blender_x_right_y_forward_z_up',
                           landmarks={n: p.array.tolist() for n, p in self.rest.landmark_positions.items()}, parts=[])
        self.path.write_text(json.dumps(self.artwork))

    def test_uniform_fit_retains_existing_geometry(self):
        result = prepare(self.path, 1.75)
        for bone in result['bones']:
            np.testing.assert_allclose(bone['fittedOriginMeters'], np.asarray(bone['origin']) * 1.75, atol=1e-14)
            self.assertAlmostEqual(bone['fittedLengthMeters'], bone['length'] * 1.75)
            self.assertEqual(bone['artworkScaleMeters'], 1.75)

    def test_independent_scales_use_parent_attachment_and_preserve_artwork(self):
        scales = {name: 1600. + index * 11 for index, name in enumerate(self.skeleton.segments)}
        result = prepare(self.path, 1.75, segment_scales_mm=scales)
        bones = {bone['name']: bone for bone in result['bones']}
        for name, bone in bones.items():
            self.assertAlmostEqual(bone['artworkScaleMeters'], scales[name] / 1000.)
            parent = self.rest.parents[name]
            if parent is None:
                np.testing.assert_array_equal(bone['fittedOriginMeters'], [0, 0, 0])
            else:
                attachment = self.skeleton.landmarks[self.rest.connect_ats[name]].local_position.array
                offset = self.rest.segment_orientations[parent].rotate_vector(vector=attachment) * scales[parent] / 1000.
                np.testing.assert_allclose(np.asarray(bone['fittedOriginMeters']) - bones[parent]['fittedOriginMeters'], offset, atol=1e-14)
        self.assertEqual(result['artwork'], self.artwork)
        self.assertEqual(json.loads(self.path.read_text()), self.artwork)
        self.assertEqual(result['fitMode'], 'recorded_segment_scales')

    def test_missing_or_invalid_fit_is_not_silently_replaced(self):
        scales = {name: 1750. for name in self.skeleton.segments}
        with self.assertRaises(ValueError):
            prepare(self.path, 1.75, segment_scales_mm={})
        scales['skull'] = float('nan')
        with self.assertRaises(ValueError):
            prepare(self.path, 1.75, segment_scales_mm=scales)


if __name__ == '__main__':
    unittest.main()
