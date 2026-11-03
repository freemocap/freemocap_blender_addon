"""Host-side protocol boundary regressions; requires an installed public Forge."""
import unittest

import numpy as np

from prepare_skelly_vrm import coordinate_bindings, humanoid_bindings


class CoordinateBoundaryTests(unittest.TestCase):
    def test_both_file_versions_import_into_the_same_receiver_frame(self):
        # Consumer-side reflections are independently specified by UniVRM.
        for version, reflection in [('0.0', np.diag([1, 1, -1])), ('1.0', np.diag([-1, 1, 1]))]:
            with self.subTest(version=version):
                binding = coordinate_bindings(version)
                np.testing.assert_array_equal(reflection @ binding['sourceToFile'], binding['sourceToReceiver'])

    def test_each_exporter_composes_to_its_declared_file_convention(self):
        for version in ('0.0', '1.0'):
            binding = coordinate_bindings(version)
            np.testing.assert_array_equal(np.asarray(binding['exporterOutputFromInput']) @ binding['exporterInputFromSource'], binding['sourceToFile'])

    def test_original_vrm1_facing_is_not_valid_for_vrm0_receiver(self):
        source_arm = np.array([-1., 0., 0.])
        original = np.diag([1, 1, -1]) @ np.asarray(coordinate_bindings('1.0')['sourceToFile']) @ source_arm
        required = np.asarray(coordinate_bindings('0.0')['sourceToReceiver']) @ source_arm
        self.assertAlmostEqual(float(original @ required), -1.)

    def test_versioned_thumb_names_retain_identical_source_bones(self):
        old, new = humanoid_bindings('0.0'), humanoid_bindings('1.0')
        self.assertEqual(set(old.values()), set(new.values()))
        for side in ('left', 'right'):
            self.assertEqual(old[side + 'ThumbProximal'], new[side + 'ThumbMetacarpal'])
            self.assertEqual(old[side + 'ThumbIntermediate'], new[side + 'ThumbProximal'])
            self.assertEqual(old[side + 'ThumbDistal'], new[side + 'ThumbDistal'])


if __name__ == '__main__':
    unittest.main()
