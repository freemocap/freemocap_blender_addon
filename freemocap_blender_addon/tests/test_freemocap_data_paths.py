import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
import toml

from freemocap_blender_addon.freemocap_data.freemocap_data_paths import FREEMOCAP_FOLDER_TOML, FreemocapDataPaths
from freemocap_blender_addon.utilities.custom_exceptions import DataFileNotFoundError


@pytest.fixture
def mock_freemocap_toml():
    with patch("builtins.open", mock_open(read_data=FREEMOCAP_FOLDER_TOML.read_text())):
        yield FREEMOCAP_FOLDER_TOML


def test_from_toml(mock_freemocap_toml: Path):
    tracker_type = "mediapipe"
    data_paths = FreemocapDataPaths.from_toml(mock_freemocap_toml, tracker_type)

    assert data_paths.output_data_files["body_npy_file"] == Path("mediapipe_body_3d_xyz.npy")
    assert data_paths.output_data_files["output_data.center_of_mass.total_body_center_of_mass_npy"] == Path(
        "total_body_center_of_mass_xyz.npy")


def test__convert_str_to_path():
    data = {
        "saved_data": {"csv": "some_path.csv"},
        "synchronized_videos": "videos_path",
        "annotated_videos": "annotated_videos_path"
    }
    data_paths = FreemocapDataPaths(**data)
    data_paths._convert_str_to_path()

    assert data_paths.saved_data["csv"] == Path("some_path.csv")
    assert data_paths.synchronized_videos == Path("videos_path")
    assert data_paths.annotated_videos == Path("annotated_videos_path")


def test__validate_paths_existing(tmp_path: Path):
    existing_file = tmp_path / "existing_file.txt"
    existing_file.touch()

    data = {
        "output_data_files": {"file1": existing_file},
        "saved_data": {"file2": existing_file},
        "synchronized_videos": existing_file,
        "annotated_videos": existing_file
    }
    data_paths = FreemocapDataPaths(**data)
    data_paths._validate_paths()  # Should not raise


def test__validate_paths_non_existing():
    data = {
        "output_data_files": {"file1": Path("non_existent_file.txt")},
        "saved_data": {"file2": Path("another_non_existent_file.txt")},
        "synchronized_videos": Path("yet_another_non_existent_file.txt"),
        "annotated_videos": Path("still_another_non_existent_file.txt")
    }
    data_paths = FreemocapDataPaths(**data)

    with pytest.raises(DataFileNotFoundError):
        data_paths._validate_paths()