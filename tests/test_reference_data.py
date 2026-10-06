import json
from pathlib import Path
import tempfile
import unittest

from tools import reference_data


class ReferenceDataTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.dataset = self.root / 'prepared/freemocap_test_data'
        self.recording = self.dataset / 'current/recordings/freemocap_test_data'
        self.recording.mkdir(parents=True)
        self.parquet = self.recording / 'freemocap_test_data_data.parquet'
        self.parquet.write_bytes(b'fixture: only the publication protocol is tested here')
        self.calibration = self.recording / 'calibration.toml'
        self.calibration.write_text('value = 1')
        self.ready = dict(recording=str(self.recording), identity=dict(source=dict(dataset='freemocap_test_data')),
                          result=dict(validation=dict(frames=222, parquet_sha256=reference_data.digest(self.parquet)),
                                      calibration_filename='calibration.toml', calibration_sha256=reference_data.digest(self.calibration)))
        self.marker = self.dataset / 'ready.json'
        self.marker.write_text(json.dumps(self.ready))

    def snapshot(self):
        return reference_data.snapshot(self.root / 'prepared', 'test_data', self.root / 'copies')

    def test_snapshot_copies_verified_publication_and_detects_later_changes(self):
        result = self.snapshot()
        self.assertNotEqual(result['path'], result['source'])
        reference_data.verify_unchanged([result])
        self.parquet.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'changed during tests'):
            reference_data.verify_unchanged([result])

    def test_pending_replacement_is_rejected(self):
        (self.dataset / 'replacement.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Pending'):
            self.snapshot()

    def test_media_is_copied_and_source_and_copy_are_checked(self):
        folder = self.recording / 'annotated_videos'
        folder.mkdir()
        video = folder / 'camera.MP4'
        video.write_bytes(b'opaque movie fixture')
        result = self.snapshot()
        self.assertEqual(len(result['media']), 1)
        copy = Path(result['media'][0]['path'])
        self.assertNotEqual(copy, video)
        reference_data.verify_unchanged([result])
        copy.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'video changed'):
            reference_data.verify_unchanged([result])

    def test_mismatched_parquet_hash_is_not_silently_accepted(self):
        self.parquet.write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.snapshot()

    def test_recording_path_cannot_escape_published_current(self):
        self.ready['recording'] = str(self.root)
        self.marker.write_text(json.dumps(self.ready))
        with self.assertRaises(ValueError):
            self.snapshot()


if __name__ == '__main__':
    unittest.main()
