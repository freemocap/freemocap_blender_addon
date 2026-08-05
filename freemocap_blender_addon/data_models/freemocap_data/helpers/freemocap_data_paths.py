from dataclasses import dataclass
from pathlib import Path
from typing import Union


def get_hand_file_with_fallback(
        folder: Path,
        filename: str,
        legacy_filename: str,
) -> Path:

    filepath = folder / filename

    if filepath.exists():
        return filepath

    legacy_filepath = folder / legacy_filename
    if legacy_filepath.exists():
        return legacy_filepath

    raise FileNotFoundError(f"Neither {filepath} nor {legacy_filepath} exist")



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

    @classmethod
    def from_recording_folder(cls, path: str):
        recording_path = Path(path)
        output_data_path = recording_path / "output_data"

        # TODO: we may want a better form of backwards compatibility than this
        # backwards compatibility:
        center_of_mass_path = output_data_path / "mediapipe_body_total_body_center_of_mass.npy"


        segment_centers_of_mass_path = output_data_path / "mediapipe_body_segment_center_of_mass.npy"

        right_hand_npy = get_hand_file_with_fallback(
            output_data_path,
            "mediapipe_right_hand_3d_xyz.npy",
            "mediapipe_right_hand_right_hand.npy",
        )

        left_hand_npy = get_hand_file_with_fallback(
            output_data_path,
            "mediapipe_left_hand_3d_xyz.npy",
            "mediapipe_left_hand_left_hand.npy",
        )
        
        # reprojection_error_path = output_data_path / "raw_data" / "mediapipe_3dData_numFrames_numTrackedPoints_reprojectionError.npy"
        # if not reprojection_error_path.exists():
        #     reprojection_error_path = output_data_path / "raw_data" / "mediapipe3dData_numFrames_numTrackedPoints_reprojectionError.npy"
        #
        possible_calibration_files = list(recording_path.glob("*calibration.toml"))
        calibration_toml_path = str(possible_calibration_files[0]) if possible_calibration_files else None #for single-cam recording cases where there is no calibration file

    
        return cls(
            body_npy=str(output_data_path / "mediapipe_body_3d_xyz.npy"),
            right_hand_npy=str(right_hand_npy),
            left_hand_npy=str(left_hand_npy),
            face_npy=str(output_data_path / "mediapipe_face_3d_xyz.npy"),

            center_of_mass_npy=str(center_of_mass_path),
            segment_centers_of_mass_npy=str(segment_centers_of_mass_path),
            #
            # reprojection_error_npy=str(
            #     reprojection_error_path),

            calibration_toml= calibration_toml_path
        )

    @staticmethod
    def _validate_recording_path(recording_path: Union[str, Path]):
        if recording_path == "":
            print("No recording path specified")
            raise FileNotFoundError("No recording path specified")

        if not Path(recording_path).exists():
            print(f"Recording path {recording_path} does not exist")
            raise FileNotFoundError(f"Recording path {recording_path} does not exist")

    def __post_init__(self):
        for path in self.__dict__.values():
            if path is None:
                continue 
            if not Path(path).exists():
                print(f"Path {path} does not exist")
                raise FileNotFoundError(f"Path {path} does not exist")
