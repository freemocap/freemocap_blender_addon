from ajc27_freemocap_blender_addon.core_functions.create_rig.add_rig_bone_method import add_rig_by_bone
from ajc27_freemocap_blender_addon.core_functions.create_rig.add_rig_method_enum import AddRigMethods
from ajc27_freemocap_blender_addon.core_functions.create_rig.add_rig_rigify_method import add_rig_rigify
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType


def add_rig_by_method(add_rig_method, bone_data, keep_symmetry, parent_object, rig_name):
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
            pose=PoseType.FREEMOCAP_TPOSE,
            add_ik_constraints=False,
        )
    else:
        raise ValueError(f"Invalid add rig method: {add_rig_method}")
    return rig
