from dataclasses import dataclass, field


@dataclass
class AdjustEmpties:
    vertical_align_reference: str = "left_knee"
    vertical_align_angle_offset: float = 0.0
    ground_align_reference: str = "left_foot_index"
    vertical_align_position_offset: float = 0.0
    correct_fingers_empties: bool = True
    add_hand_middle_empty: bool = True


@dataclass
class ReduceBoneLengthDispersion:
    interval_variable: str = "median"
    interval_factor: float = 0.0


@dataclass
class ReduceShakiness:
    recording_fps: float = 30.0


@dataclass
class AddRig:
    bone_length_method: str = "median_length"
    keep_symmetry: bool = False
    add_fingers_constraints: bool = True
    use_limit_rotation: bool = False
    """Rest pose the armature is built in: 'tpose' or 'apose'."""
    rest_pose: str = "tpose"


@dataclass
class AddBodyMesh:
    body_mesh_mode: str = "custom"


@dataclass
class Export3DModel:
    """Options for `MainController.export_3d_model()` (= `export_3d_model()`).

    `formats` may be empty, in which case the 3D model export stage is skipped.
    """

    formats: list[str] = field(default_factory=lambda: ["fbx", "bvh"])


@dataclass
class MotionCleanup:
    """Cleanup applied to the marker motion before the scene is set up."""

    """If True, run `MainController.apply_foot_locking()` on the marker empties."""
    apply_foot_locking: bool = False
    """If True, run `MainController.limit_hand_markers_range_of_motion()` on the marker empties."""
    limit_hand_markers_range_of_motion: bool = False


@dataclass
class Config:
    adjust_empties: AdjustEmpties = field(default_factory=AdjustEmpties)
    reduce_bone_length_dispersion: ReduceBoneLengthDispersion = field(default_factory=ReduceBoneLengthDispersion)
    reduce_shakiness: ReduceShakiness = field(default_factory=ReduceShakiness)
    add_rig: AddRig = field(default_factory=AddRig)
    add_body_mesh: AddBodyMesh = field(default_factory=AddBodyMesh)
    export_3d_model: Export3DModel = field(default_factory=Export3DModel)
    motion_cleanup: MotionCleanup = field(default_factory=MotionCleanup)
