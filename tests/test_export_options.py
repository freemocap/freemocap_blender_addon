import unittest
from freemocap_blender_addon.export_options import parquet_options
from freemocap_blender_addon.data_models.parameter_models.load_parameters_config import load_parameters_config_from_dict


class OptionsTests(unittest.TestCase):
    def test_main_configuration_sections(self):
        config = load_parameters_config_from_dict(dict(add_rig=dict(rest_pose='apose'),
            export_3d_model=dict(formats=[]), motion_cleanup=dict(apply_foot_locking=True)))
        self.assertEqual(config.add_rig.rest_pose, 'apose')
        self.assertEqual(config.export_3d_model.formats, [])
        self.assertTrue(config.motion_cleanup.apply_foot_locking)
        self.assertFalse(config.motion_cleanup.limit_hand_markers_range_of_motion)

    def test_parquet_capabilities_reject_unsupported_requests(self):
        for route, config in [
            ('parquet_segments', {'motion_cleanup': {'apply_foot_locking': True}}),
            ('parquet_segments', {'add_rig': {'rest_pose': 'apose'}}),
            ('parquet_constraints', {'export_3d_model': {'formats': ['unsupported']}}),
            ('parquet_constraints', {'reduce_shakiness': {}}),
        ]:
            with self.subTest(route=route, config=config), self.assertRaises(ValueError):
                parquet_options(route, config)
        self.assertEqual(parquet_options('parquet_constraints', {'add_rig': {'rest_pose': 'apose'}})['rest_pose'], 'apose')

    def test_defaults_do_not_request_cleanup_or_sidecar_exports(self):
        options = parquet_options('parquet_segments', {})
        self.assertEqual(options['formats'], [])
        self.assertFalse(options['foot_locking'])
        self.assertFalse(options['hand_limits'])

    def test_both_parquet_routes_support_blender_fbx_and_bvh(self):
        for route in ('parquet_segments', 'parquet_constraints'):
            for formats in (['bvh'], ['fbx'], ['fbx', 'bvh']):
                with self.subTest(route=route, formats=formats):
                    self.assertEqual(parquet_options(route,
                        {'export_3d_model': {'formats': formats}})['formats'], formats)


class FramerateTests(unittest.TestCase):
    def test_legacy_timestamp_rate_and_missing_input(self):
        import tempfile
        from pathlib import Path
        from freemocap_blender_addon.utilities.recording_framerate import get_recording_framerate
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertIsNone(get_recording_framerate(root))
            timestamps = root / 'synchronized_videos/timestamps/camera_timestamps.csv'
            timestamps.parent.mkdir(parents=True)
            timestamps.write_text('frame_duration_ms\n' + '16.68335\n' * 12)
            self.assertAlmostEqual(get_recording_framerate(root), 59.94, places=3)

