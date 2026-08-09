from dataclasses import dataclass
from pathlib import Path
from typing import Union


# Per-detector filename suffixes. The body/face/centre-of-mass names differ only by prefix,
# but the hand files do not follow the same convention between detectors, so each is listed.
_DETECTOR_FILES = {
    "rtmpose": {
        "body": "rtmpose_body_3d_xyz.npy",
        "right_hand": "rtmpose_right_hand_3d_xyz.npy",
        "left_hand": "rtmpose_left_hand_3d_xyz.npy",
        "face": "rtmpose_face_3d_xyz.npy",
        "com": "rtmpose_body_total_body_center_of_mass.npy",
        "segment_com": "rtmpose_body_segment_center_of_mass.npy",
    },
    "mediapipe": {
        "body": "mediapipe_body_3d_xyz.npy",
        "right_hand": "mediapipe_right_hand_3d_xyz.npy",
        "left_hand": "mediapipe_left_hand_3d_xyz.npy",
        "face": "mediapipe_face_3d_xyz.npy",
        "com": "mediapipe_body_total_body_center_of_mass.npy",
        "segment_com": "mediapipe_body_segment_center_of_mass.npy",
    },
}

# Hand files were renamed to the `*_3d_xyz.npy` convention; recordings processed before
# that still carry the doubled-up name. Fall back so older recordings keep loading.
_LEGACY_FILENAMES = {
    "mediapipe_right_hand_3d_xyz.npy": "mediapipe_right_hand_right_hand.npy",
    "mediapipe_left_hand_3d_xyz.npy": "mediapipe_left_hand_left_hand.npy",
    "rtmpose_right_hand_3d_xyz.npy": "rtmpose_right_hand_right_hand.npy",
    "rtmpose_left_hand_3d_xyz.npy": "rtmpose_left_hand_left_hand.npy",
}


def _resolve(output_data_path: Path, filename: str) -> Path:
    """Path to `filename`, falling back to its pre-rename spelling if that is what exists."""
    path = output_data_path / filename
    if path.exists():
        return path
    legacy = _LEGACY_FILENAMES.get(filename)
    if legacy is not None:
        legacy_path = output_data_path / legacy
        if legacy_path.exists():
            return legacy_path
    return path


def detect_data_source(output_data_path: Path) -> str:
    """Which detector produced this recording's output.

    A recording can contain both if it was reprocessed, so prefer rtmpose - it is FreeMoCap's
    default and the more accurate of the two.
    """
    for source in ("rtmpose", "mediapipe"):
        if (output_data_path / _DETECTOR_FILES[source]["body"]).exists():
            return source
    raise FileNotFoundError(
        f"No recognised body data in {output_data_path}. Expected one of: "
        + ", ".join(_DETECTOR_FILES[s]["body"] for s in _DETECTOR_FILES)
    )


@dataclass
class FreemocapDataPaths:
    body_npy: str
    right_hand_npy: str
    left_hand_npy: str
    face_npy: str
    center_of_mass_npy: str
    segment_centers_of_mass_npy: str
    # reprojection_error_npy: str
    calibration_toml: str | None
    data_source: str = "mediapipe"

    @classmethod
    def from_recording_folder(cls, path: str, data_source: str | None = None):
        recording_path = Path(path)
        output_data_path = recording_path / "output_data"

        if data_source is None:
            data_source = detect_data_source(output_data_path)
        files = _DETECTOR_FILES[data_source]

        center_of_mass_path = output_data_path / files["com"]
        segment_centers_of_mass_path = output_data_path / files["segment_com"]

        
        # reprojection_error_path = output_data_path / "raw_data" / "mediapipe_3dData_numFrames_numTrackedPoints_reprojectionError.npy"
        # if not reprojection_error_path.exists():
        #     reprojection_error_path = output_data_path / "raw_data" / "mediapipe3dData_numFrames_numTrackedPoints_reprojectionError.npy"
        #
        possible_calibration_files = list(recording_path.glob("*calibration.toml"))
        calibration_toml_path = str(possible_calibration_files[0]) if possible_calibration_files else None #for single-cam recording cases where there is no calibration file

        return cls(
            body_npy=str(_resolve(output_data_path, files["body"])),
            right_hand_npy=str(_resolve(output_data_path, files["right_hand"])),
            left_hand_npy=str(_resolve(output_data_path, files["left_hand"])),
            face_npy=str(_resolve(output_data_path, files["face"])),

            center_of_mass_npy=str(center_of_mass_path),
            segment_centers_of_mass_npy=str(segment_centers_of_mass_path),
            #
            # reprojection_error_npy=str(
            #     reprojection_error_path),

            calibration_toml=calibration_toml_path,
            data_source=data_source,
        )

    @staticmethod
    def _validate_recording_path(recording_path: Union[str, Path]):
        if recording_path == "":
            print("No recording path specified")
            raise FileNotFoundError("No recording path specified")

        if not Path(recording_path).exists():
            print(f"Recording path {recording_path} does not exist")
            raise FileNotFoundError(f"Recording path {recording_path} does not exist")

    # Fields on this dataclass that are not filesystem paths and must not be stat'd.
    _NON_PATH_FIELDS = frozenset({"data_source"})

    def __post_init__(self):
        for name, path in self.__dict__.items():
            if name in self._NON_PATH_FIELDS or path is None:
                continue
            if not Path(path).exists():
                print(f"Path {path} does not exist")
                raise FileNotFoundError(f"Path {path} does not exist")
