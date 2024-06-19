from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
from freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths import FreemocapDataPaths

VALID_NPY_DATA: np.ndarray = np.array([1, 2, 3])


@pytest.fixture
def mock_path_exists() -> MagicMock:
    with patch('freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths.Path.exists',
               return_value=True) as mock_exists:
        yield mock_exists


def test_freemocap_npy_paths_initialization(recording_path_fixture: str) -> None:
    paths: FreemocapDataPaths = FreemocapDataPaths.from_recording_path(path=str(recording_path_fixture))
    assert paths.recording_folder_path == recording_path_fixture
    assert Path(paths.skeleton.body).exists()
    assert Path(paths.skeleton.hands.right).exists()
    assert Path(paths.skeleton.hands.left).exists()
    assert Path(paths.skeleton.face).exists()
    assert Path(paths.skeleton.reprojection_error).exists()
    assert Path(paths.center_of_mass.total_body_center_of_mass).exists()
    assert Path(paths.center_of_mass.segment_center_of_mass).exists()
    assert Path(paths.video.raw.path).exists()
    assert Path(paths.video.annotated.path).exists()


def test_file_not_found_error(tmp_path: Path) -> None:
    with patch('freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths.Path.exists',
               return_value=False):
        with pytest.raises(FileNotFoundError):
            FreemocapDataPaths.from_recording_path(path=str(tmp_path))
