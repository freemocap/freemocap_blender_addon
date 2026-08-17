import bpy
from freemocap_blender_addon.data_models.bones.bone_definitions import (
    is_hand_bone,
)

def get_bone_info(armature):

    # Calculate bone positions and store them in the dictionary
    bone_info = {}

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in armature.data.edit_bones:
        bone_info[bone.name] = {
            'head_position': bone.head.copy(),
            'tail_position': bone.tail.copy(),
            'length': bone.length,
            'roll': bone.roll
        }

    # Return to Object Mode after calculating bone positions
    bpy.ops.object.mode_set(mode='OBJECT')

    return bone_info


def align_markers_to_armature(
    markers_list,
    markers_reference,
    bone_info
) -> None:
    # Move the empty markers to make the T-Pose in frame 0
    for marker, info in markers_reference.items():
        bone_name = info["bone"]

        try:
            bone = bone_info[bone_name]

        except KeyError:
            if is_hand_bone(bone_name):
                print(
                    f"Skipping marker '{marker}': "
                    f"hand bone '{bone_name}' does not exist."
                )
                continue

            raise

        target_marker = [
            obj for obj in markers_list
            if marker in obj.name
        ][0]

        if info["at_head"]:
            target_marker.location = bone["head_position"]
        else:
            target_marker.location = bone["tail_position"]

    return