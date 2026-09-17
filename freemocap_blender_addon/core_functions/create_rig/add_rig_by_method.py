from freemocap_blender_addon.core_functions.create_rig.add_rig_bone_method import add_rig_by_bone
from freemocap_blender_addon.core_functions.create_rig.add_rig_method_enum import AddRigMethods
from freemocap_blender_addon.core_functions.create_rig.add_rig_rigify_method import add_rig_rigify
from freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType

DEFAULT_REST_POSE = "tpose"

# Maps the `rest_pose` config option to the armature pose definition it selects.
_POSE_BY_REST_POSE = {
    "tpose": PoseType.FREEMOCAP_TPOSE,
    "apose": PoseType.FREEMOCAP_APOSE,
}


def pose_from_rest_pose(rest_pose: str):
    """Resolve a `rest_pose` config value to the armature pose definition it selects.

    Single source of truth for the mapping, so the rig construction and the bone
    constraints it is paired with can never disagree on the pose.
    """
    pose = _POSE_BY_REST_POSE.get(rest_pose)
    if pose is None:
        print(f"Unknown rest_pose '{rest_pose}'; falling back to '{DEFAULT_REST_POSE}'")
        pose = _POSE_BY_REST_POSE[DEFAULT_REST_POSE]
    return pose


def add_rig_by_method(add_rig_method, bone_data, keep_symmetry, parent_object, rig_name, rest_pose: str = DEFAULT_REST_POSE):
    if add_rig_method == AddRigMethods.RIGIFY:
        rig = add_rig_rigify(
            bone_data=bone_data,
            rig_name=rig_name,
            parent_object=parent_object,
            keep_symmetry=keep_symmetry,
        )
    elif add_rig_method == AddRigMethods.BY_BONE:
        rig = add_rig_by_bone(
            bone_data=bone_data,
            rig_name=rig_name,
            armature_definition=ArmatureType.FREEMOCAP,
            pose=pose_from_rest_pose(rest_pose),
            add_ik_constraints=False,
        )
    else:
        raise ValueError(f"Invalid add rig method: {add_rig_method}")
    return rig
