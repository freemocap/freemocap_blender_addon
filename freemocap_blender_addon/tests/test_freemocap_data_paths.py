from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pytest

from freemocap_blender_addon.freemocap_data.freemocap_data_paths import FreemocapNpyPaths, TrackerType

VALID_NPY_DATA: np.ndarray = np.array([1, 2, 3])


@pytest.fixture
def mock_np_load() -> MagicMock:
    with patch('freemocap_blender_addon.freemocap_data.freemocap_data_paths.np.load',
               return_value=VALID_NPY_DATA) as mock_load:
        yield mock_load


@pytest.fixture
def mock_path_exists() -> MagicMock:
    with patch('freemocap_blender_addon.freemocap_data.freemocap_data_paths.Path.exists',
               return_value=True) as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_is_file() -> MagicMock:
    with patch('freemocap_blender_addon.freemocap_data.freemocap_data_paths.Path.is_file',
               return_value=True) as mock_is_file:
        yield mock_is_file


def test_freemocap_npy_paths_initialization(tmp_path: Path, mock_path_exists: MagicMock,
                                            mock_np_load: MagicMock) -> None:
    paths: FreemocapNpyPaths = FreemocapNpyPaths.from_recording_path(path=str(tmp_path))
    assert paths.recording_folder_path == tmp_path
    assert paths.skeleton.body.exists()
    assert paths.skeleton.hands.right.exists()
    assert paths.skeleton.hands.left.exists()
    assert paths.skeleton.face.exists()
    assert paths.skeleton.reprojection_error.exists()
    assert paths.center_of_mass.total_body_center_of_mass.exists()
    assert paths.center_of_mass.segment_center_of_mass.exists()
    assert paths.video.raw.exists()
    assert paths.video.annotated.exists()


def test_file_not_found_error(tmp_path: Path) -> None:
    with patch('freemocap_blender_addon.freemocap_data.freemocap_data_paths.Path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            FreemocapNpyPaths.from_recording_path(path=str(tmp_path))


def test_empty_npy_file_error(tmp_path: Path, mock_path_exists: MagicMock) -> None:
    with patch('freemocap_blender_addon.freemocap_data.freemocap_data_paths.np.load', return_value=np.array([])):
        with pytest.raises(ValueError, match="Empty npy file"):
            FreemocapNpyPaths.from_recording_path(path=str(tmp_path))


def test_placeholder_replacement(tmp_path: Path, mock_path_exists: MagicMock, mock_np_load: MagicMock) -> None:
    paths: FreemocapNpyPaths = FreemocapNpyPaths.from_recording_path(path=str(tmp_path))
    assert str(paths.skeleton.body).startswith(str(tmp_path))
    assert str(paths.skeleton.hands.right).startswith(str(tmp_path))
    assert str(paths.skeleton.hands.left).startswith(str(tmp_path))
    assert str(paths.skeleton.face).startswith(str(tmp_path))
    assert str(paths.skeleton.reprojection_error).startswith(str(tmp_path))
    assert str(paths.center_of_mass.total_body_center_of_mass).startswith(str(tmp_path))
    assert str(paths.center_of_mass.segment_center_of_mass).startswith(str(tmp_path))
    assert str(paths.video.raw).startswith(str(tmp_path))
    assert str(paths.video.annotated).startswith(str(tmp_path))


def test_integration_workflow(tmp_path: Path, mock_path_exists: MagicMock, mock_np_load: MagicMock) -> None:
    paths: FreemocapNpyPaths = FreemocapNpyPaths.from_recording_path(path=str(tmp_path),
                                                                     tracker_type=TrackerType.MEDIAPIPE)
    assert isinstance(paths, FreemocapNpyPaths)
