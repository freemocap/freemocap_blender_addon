from enum import Enum
import math as m
import re
from typing import Dict, List, Optional
from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import ArmatureBoneInfo
from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement
import bpy
import mathutils
import addon_utils

from ajc27_freemocap_blender_addon.system.constants import (
    FREEMOCAP_ARMATURE,
    UE_METAHUMAN_SIMPLE_ARMATURE,
    FREEMOCAP_TPOSE,
    FREEMOCAP_APOSE,
    UE_METAHUMAN_DEFAULT,
    UE_METAHUMAN_TPOSE,
)
from ajc27_freemocap_blender_addon.data_models.bones.bone_constraints import (
    ALL_BONES_CONSTRAINT_DEFINITIONS,
    ConstraintType,
    CopyLocationConstraint,
    DampedTrackConstraint,
    IKConstraint,
    LimitRotationConstraint,
    LockedTrackConstraint,
)
from ajc27_freemocap_blender_addon.data_models.bones.ik_control_bones import (
    ik_control_bones,
)
from ajc27_freemocap_blender_addon.data_models.bones.ik_pole_bones import ik_pole_bones
from ajc27_freemocap_blender_addon.data_models.armatures.bone_name_map import (
    bone_name_map,
)
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType


class AddRigMethods(Enum):
    RIGIFY = "rigify"
    BY_BONE = "by_bone"

def add_rig(
    bone_data: Dict[str, Dict[str, float]],
    rig_name: str,
    parent_object: bpy.types.Object,
    add_rig_method: AddRigMethods = AddRigMethods.BY_BONE,
    keep_symmetry: bool = False,
    add_fingers_constraints: bool = False,
    use_limit_rotation: bool = False,
) -> bpy.types.Object:

    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

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
            armature=ArmatureType.FREEMOCAP,
            pose=PoseType.FREEMOCAP_TPOSE,
            add_ik_constraints=False,
        )
    else:
        raise ValueError(f"Invalid add rig method: {add_rig_method}")

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # TODO: make sure this still adds constraints properly
    add_constraints(
        rig=rig,
        add_fingers_constraints=add_fingers_constraints,
        parent_object=parent_object,
        armature=ArmatureType.FREEMOCAP,
        pose=PoseType.FREEMOCAP_TPOSE,
        use_limit_rotation=use_limit_rotation,
    )

    ### Bake animation to the rig ###
    # Get the empties ending frame
    ending_frame = int(bpy.data.actions[0].frame_range[1])
    # Bake animation
    bpy.ops.nla.bake(frame_start=1, frame_end=ending_frame, bake_types={"POSE"})

    # Change back to Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    return rig


def add_rig_rigify(
    bone_data: Dict[str, Dict[str, float]],
    rig_name: str,
    parent_object: bpy.types.Object,
    keep_symmetry: bool = False,
) -> bpy.types.Object:
    ensure_rigify()

    try:
        bpy.ops.object.armature_human_metarig_add()
    except Exception as e:
        raise e

    # Rename metarig armature to rig_name
    bpy.data.armatures[0].name = rig_name
    # Get reference to armature
    rig = bpy.data.objects["metarig"]
    # Rename the rig object to root
    rig.name = rig_name
    rig.data.display_type = "STICK"
    # Get reference to the renamed armature
    rig = bpy.data.objects[rig_name]
    rig.parent = parent_object

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")
    # Select the only the rig
    rig.select_set(True)

    # Get rig height as the sum of the major bones length in a standing position. Assume foot declination angle of 23º
    avg_ankle_projection_length = (
        m.sin(m.radians(23)) * bone_data["foot.R"]["median"]
        + m.sin(m.radians(23)) * bone_data["foot.L"]["median"]
    ) / 2
    avg_shin_length = (
        bone_data["shin.R"]["median"] + bone_data["shin.L"]["median"]
    ) / 2
    avg_thigh_length = (
        bone_data["thigh.R"]["median"] + bone_data["thigh.L"]["median"]
    ) / 2

    rig_height = (
        avg_ankle_projection_length
        + avg_shin_length
        + avg_thigh_length
        + bone_data["spine"]["median"]
        + bone_data["spine.001"]["median"]
        + bone_data["neck"]["median"]
    )

    # Calculate new rig proportion
    rig_new_proportion = rig_height / rig.dimensions.z
    # Scale the rig by the new proportion
    rig.scale = (rig_new_proportion, rig_new_proportion, rig_new_proportion)

    # Apply transformations to rig (scale must be (1, 1, 1) so it doesn't fail on send2ue export
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Get references to the different rig bones
    bpy.ops.object.mode_set(mode="EDIT")

    spine = rig.data.edit_bones["spine"]
    spine_003 = rig.data.edit_bones["spine.003"]
    spine_004 = rig.data.edit_bones["spine.004"]
    spine_005 = rig.data.edit_bones["spine.005"]
    spine_006 = rig.data.edit_bones["spine.006"]
    face = rig.data.edit_bones["face"]
    nose = rig.data.edit_bones["nose"]
    breast_R = rig.data.edit_bones["breast.R"]
    breast_L = rig.data.edit_bones["breast.L"]
    shoulder_R = rig.data.edit_bones["shoulder.R"]
    shoulder_L = rig.data.edit_bones["shoulder.L"]
    upper_arm_R = rig.data.edit_bones["upper_arm.R"]
    upper_arm_L = rig.data.edit_bones["upper_arm.L"]
    forearm_R = rig.data.edit_bones["forearm.R"]
    forearm_L = rig.data.edit_bones["forearm.L"]
    hand_R = rig.data.edit_bones["hand.R"]
    hand_L = rig.data.edit_bones["hand.L"]
    pelvis_R = rig.data.edit_bones["pelvis.R"]
    pelvis_L = rig.data.edit_bones["pelvis.L"]
    thigh_R = rig.data.edit_bones["thigh.R"]
    thigh_L = rig.data.edit_bones["thigh.L"]
    shin_R = rig.data.edit_bones["shin.R"]
    shin_L = rig.data.edit_bones["shin.L"]
    foot_R = rig.data.edit_bones["foot.R"]
    foot_L = rig.data.edit_bones["foot.L"]
    toe_R = rig.data.edit_bones["toe.R"]
    toe_L = rig.data.edit_bones["toe.L"]
    heel_02_R = rig.data.edit_bones["heel.02.R"]
    heel_02_L = rig.data.edit_bones["heel.02.L"]

    # Get the hips_center z position as the sum of heel, shin and thigh lengths
    hips_center_z_pos = avg_ankle_projection_length + avg_shin_length + avg_thigh_length

    # Move the spine and pelvis bone heads to the point (0, 0, hips_center_z_pos)
    spine.head = (0, 0, hips_center_z_pos)
    pelvis_R.head = (0, 0, hips_center_z_pos)
    pelvis_L.head = (0, 0, hips_center_z_pos)

    # Calculate the average length of the pelvis bones
    avg_pelvis_length = (
        bone_data["pelvis.R"]["median"] + bone_data["pelvis.L"]["median"]
    ) / 2

    # Set the pelvis bones length based on the keep symmetry parameter
    pelvis_R_length = (
        avg_pelvis_length if keep_symmetry else bone_data["pelvis.R"]["median"]
    )
    pelvis_L_length = (
        avg_pelvis_length if keep_symmetry else bone_data["pelvis.L"]["median"]
    )

    # Align the pelvis bone tails to the hips center
    pelvis_R.tail = (-pelvis_R_length, 0, hips_center_z_pos)
    pelvis_L.tail = (pelvis_L_length, 0, hips_center_z_pos)
    # Reset pelvis bones rotations
    pelvis_R.roll = 0
    pelvis_L.roll = 0

    # Move thighs bone head to the position of corresponding pelvis bone tail
    thigh_R.head = (-pelvis_R_length, 0, hips_center_z_pos)
    thigh_L.head = (pelvis_L_length, 0, hips_center_z_pos)

    # Set the thigh bones length based on the keep symmetry parameter
    thigh_R_length = (
        avg_thigh_length if keep_symmetry else bone_data["thigh.R"]["median"]
    )
    thigh_L_length = (
        avg_thigh_length if keep_symmetry else bone_data["thigh.L"]["median"]
    )

    # Align the thighs bone tail to the bone head
    thigh_R.tail = (-pelvis_R_length, 0, hips_center_z_pos - thigh_R_length)
    thigh_L.tail = (pelvis_L_length, 0, hips_center_z_pos - thigh_L_length)

    # Set the shin bones length based on the keep symmetry parameter
    shin_R_length = avg_shin_length if keep_symmetry else bone_data["shin.R"]["median"]
    shin_L_length = avg_shin_length if keep_symmetry else bone_data["shin.L"]["median"]

    # Align the shin bones to the thigh bones
    shin_R.tail = (
        -pelvis_R_length,
        0,
        hips_center_z_pos - thigh_R_length - shin_R_length,
    )
    shin_L.tail = (
        pelvis_L_length,
        0,
        hips_center_z_pos - thigh_L_length - shin_L_length,
    )

    # Remove the toe bones
    rig.data.edit_bones.remove(rig.data.edit_bones["toe.R"])
    rig.data.edit_bones.remove(rig.data.edit_bones["toe.L"])

    # Move the foot bones tail to adjust their length depending on keep symmetry and also form a 23º degree with the horizontal plane
    avg_foot_length = (
        bone_data["foot.R"]["median"] + bone_data["foot.L"]["median"]
    ) / 2

    # Set the foot bones length based on the keep symmetry parameter
    foot_R_length = avg_foot_length if keep_symmetry else bone_data["foot.R"]["median"]
    foot_L_length = avg_foot_length if keep_symmetry else bone_data["foot.L"]["median"]

    foot_R.tail = (
        -pelvis_R_length,
        -foot_R_length * m.cos(m.radians(23)),
        foot_R.head[2] - foot_R_length * m.sin(m.radians(23)),
    )
    foot_L.tail = (
        pelvis_L_length,
        -foot_L_length * m.cos(m.radians(23)),
        foot_L.head[2] - foot_L_length * m.sin(m.radians(23)),
    )

    # Move the heel bones so their head is aligned with the ankle on the x axis
    avg_heel_length = (
        bone_data["heel.02.R"]["median"] + bone_data["heel.02.L"]["median"]
    ) / 2

    # Set the heel bones length based on the keep symmetry parameter
    heel_02_R_length = (
        avg_heel_length if keep_symmetry else bone_data["heel.02.R"]["median"]
    )
    heel_02_L_length = (
        avg_heel_length if keep_symmetry else bone_data["heel.02.L"]["median"]
    )

    heel_02_R.head = (-pelvis_R_length, heel_02_R.head[1], heel_02_R.head[2])
    heel_02_R.length = heel_02_R_length
    heel_02_L.head = (pelvis_L_length, heel_02_L.head[1], heel_02_L.head[2])
    heel_02_L.length = heel_02_L_length

    # Make the heel bones be connected with the shin bones
    heel_02_R.parent = shin_R
    heel_02_R.use_connect = True
    heel_02_L.parent = shin_L
    heel_02_L.use_connect = True

    # Add a pelvis bone to the root and then make it the parent of spine, pelvis.R and pelvis.L bones
    pelvis = rig.data.edit_bones.new("pelvis")
    pelvis.head = spine.head
    pelvis.tail = spine.head + mathutils.Vector([0, 0.1, 0])

    # Change the pelvis.R, pelvis.L, thigh.R, thigh.L and spine parent to the new pelvis bone
    pelvis_R.parent = pelvis
    pelvis_R.use_connect = False
    pelvis_L.parent = pelvis
    pelvis_L.use_connect = False
    thigh_R.parent = pelvis
    thigh_R.use_connect = False
    thigh_L.parent = pelvis
    thigh_L.use_connect = False
    spine.parent = pelvis
    spine.use_connect = False

    # Change parent of spine.003 bone to spine to erase bones spine.001 and spine.002
    spine_003.parent = spine
    spine_003.use_connect = True
    # Remove spine.001 and spine.002 bones
    rig.data.edit_bones.remove(rig.data.edit_bones["spine.001"])
    rig.data.edit_bones.remove(rig.data.edit_bones["spine.002"])

    # Rename spine.003 to spine.001
    rig.data.edit_bones["spine.003"].name = "spine.001"
    spine_001 = rig.data.edit_bones["spine.001"]

    # Adjust the spine bone length and align it vertically
    spine.tail = (
        spine.head[0],
        spine.head[1],
        spine.head[2] + bone_data["spine"]["median"],
    )

    # Adjust the spine.001 bone length and align it vertically
    spine_001.tail = (
        spine_001.head[0],
        spine_001.head[1],
        spine_001.head[2] + bone_data["spine.001"]["median"],
    )

    # Calculate the shoulders head z offset from the spine.001 tail. This to raise the shoulders and breasts by that offset
    shoulder_z_offset = spine_001.tail[2] - shoulder_R.head[2]

    # Raise breasts and shoulders by the z offset
    breast_R.head[2] += shoulder_z_offset
    breast_R.tail[2] += shoulder_z_offset
    breast_L.head[2] += shoulder_z_offset
    breast_L.tail[2] += shoulder_z_offset
    shoulder_R.head[2] += shoulder_z_offset
    shoulder_R.tail[2] += shoulder_z_offset
    shoulder_L.head[2] += shoulder_z_offset
    shoulder_L.tail[2] += shoulder_z_offset

    # Get average shoulder length
    avg_shoulder_length = (
        bone_data["shoulder.R"]["median"] + bone_data["shoulder.L"]["median"]
    ) / 2

    # Set the shoulder bones length based on the keep symmetry parameter
    shoulder_R_length = (
        avg_shoulder_length if keep_symmetry else bone_data["shoulder.R"]["median"]
    )
    shoulder_L_length = (
        avg_shoulder_length if keep_symmetry else bone_data["shoulder.L"]["median"]
    )

    # Move the shoulder tail in the x axis
    shoulder_R.tail[0] = spine_001.tail[0] - shoulder_R_length
    shoulder_L.tail[0] = spine_001.tail[0] + shoulder_L_length

    # Calculate the upper_arms head x and z offset from the shoulder_R tail. This to raise and adjust the arms and hands by that offset
    upper_arm_R_x_offset = shoulder_R.tail[0] - upper_arm_R.head[0]
    upper_arm_R_z_offset = spine_001.tail[2] - upper_arm_R.head[2]
    upper_arm_L_x_offset = shoulder_L.tail[0] - upper_arm_L.head[0]
    upper_arm_L_z_offset = spine_001.tail[2] - upper_arm_L.head[2]

    upper_arm_R.head[2] += upper_arm_R_z_offset
    upper_arm_R.tail[2] += upper_arm_R_z_offset
    upper_arm_R.head[0] += upper_arm_R_x_offset
    upper_arm_R.tail[0] += upper_arm_R_x_offset
    for bone_constraint_definition in upper_arm_R.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[2] += upper_arm_R_z_offset
            bone_constraint_definition.tail[2] += upper_arm_R_z_offset
            bone_constraint_definition.head[0] += upper_arm_R_x_offset
            bone_constraint_definition.tail[0] += upper_arm_R_x_offset
        else:
            bone_constraint_definition.tail[2] += upper_arm_R_z_offset
            bone_constraint_definition.tail[0] += upper_arm_R_x_offset

    upper_arm_L.head[2] += upper_arm_L_z_offset
    upper_arm_L.tail[2] += upper_arm_L_z_offset
    upper_arm_L.head[0] += upper_arm_L_x_offset
    upper_arm_L.tail[0] += upper_arm_L_x_offset
    for bone_constraint_definition in upper_arm_L.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[2] += upper_arm_L_z_offset
            bone_constraint_definition.tail[2] += upper_arm_L_z_offset
            bone_constraint_definition.head[0] += upper_arm_L_x_offset
            bone_constraint_definition.tail[0] += upper_arm_L_x_offset
        else:
            bone_constraint_definition.tail[2] += upper_arm_L_z_offset
            bone_constraint_definition.tail[0] += upper_arm_L_x_offset

    # Align the y position of breasts, shoulders, arms and hands to the y position of the spine.001 tail
    # Calculate the breasts head y offset from the spine.001 tail
    breast_y_offset = spine_001.tail[1] - breast_R.head[1]
    # Move breast by the y offset
    breast_R.head[1] += breast_y_offset
    breast_R.tail[1] += breast_y_offset
    breast_L.head[1] += breast_y_offset
    breast_L.tail[1] += breast_y_offset

    # Temporarily remove breast bones. (Comment these lines if breast bones are needed)
    rig.data.edit_bones.remove(rig.data.edit_bones[breast_R.name])
    rig.data.edit_bones.remove(rig.data.edit_bones[breast_L.name])

    # Set the y position to which the arms bones will be aligned
    arms_bones_y_pos = spine_001.tail[1]
    # Move shoulders on y axis and also move shoulders head to the center at x=0 ,
    shoulder_R.head[1] = arms_bones_y_pos
    shoulder_R.head[0] = 0
    shoulder_R.tail[1] = arms_bones_y_pos
    shoulder_L.head[1] = arms_bones_y_pos
    shoulder_L.head[0] = 0
    shoulder_L.tail[1] = arms_bones_y_pos

    # Move upper_arm and forearm
    upper_arm_R.head[1] = arms_bones_y_pos
    upper_arm_R.tail[1] = arms_bones_y_pos
    upper_arm_L.head[1] = arms_bones_y_pos
    upper_arm_L.tail[1] = arms_bones_y_pos

    # Calculate hand head y offset to arms_bones_y_pos to move the whole hand
    hand_R_y_offset = arms_bones_y_pos - hand_R.head[1]
    hand_L_y_offset = arms_bones_y_pos - hand_L.head[1]

    # Move hands and its children by the y offset (forearm tail is moved by hand head)
    hand_R.head[1] += hand_R_y_offset
    hand_R.tail[1] += hand_R_y_offset
    for bone_constraint_definition in hand_R.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[1] += hand_R_y_offset
            bone_constraint_definition.tail[1] += hand_R_y_offset
        else:
            bone_constraint_definition.tail[1] += hand_R_y_offset

    hand_L.head[1] += hand_L_y_offset
    hand_L.tail[1] += hand_L_y_offset
    for bone_constraint_definition in hand_L.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[1] += hand_L_y_offset
            bone_constraint_definition.tail[1] += hand_L_y_offset
        else:
            bone_constraint_definition.tail[1] += hand_L_y_offset

    # Change to Pose Mode to rotate the arms and make a T Pose for posterior retargeting
    bpy.ops.object.mode_set(mode="POSE")
    pose_upper_arm_R = rig.pose.bones["upper_arm.R"]
    pose_upper_arm_R.rotation_mode = "XYZ"
    pose_upper_arm_R.rotation_euler = (0, m.radians(-7), m.radians(-29))
    pose_upper_arm_R.rotation_mode = "QUATERNION"
    pose_upper_arm_L = rig.pose.bones["upper_arm.L"]
    pose_upper_arm_L.rotation_mode = "XYZ"
    pose_upper_arm_L.rotation_euler = (0, m.radians(7), m.radians(29))
    pose_upper_arm_L.rotation_mode = "QUATERNION"
    pose_forearm_R = rig.pose.bones["forearm.R"]
    pose_forearm_R.rotation_mode = "XYZ"
    pose_forearm_R.rotation_euler = (0, 0, m.radians(-4))
    pose_forearm_R.rotation_mode = "QUATERNION"
    pose_forearm_L = rig.pose.bones["forearm.L"]
    pose_forearm_L.rotation_mode = "XYZ"
    pose_forearm_L.rotation_euler = (0, 0, m.radians(4))
    pose_forearm_L.rotation_mode = "QUATERNION"
    pose_hand_R = rig.pose.bones["hand.R"]
    pose_hand_R.rotation_mode = "XYZ"
    pose_hand_R.rotation_euler = (m.radians(-5.7), 0, m.radians(-3.7))
    pose_hand_R.rotation_mode = "QUATERNION"
    pose_hand_L = rig.pose.bones["hand.L"]
    pose_hand_L.rotation_mode = "XYZ"
    pose_hand_L.rotation_euler = (m.radians(-5.7), 0, m.radians(3.7))
    pose_hand_L.rotation_mode = "QUATERNION"
    pose_thigh_R = rig.pose.bones["thigh.R"]
    pose_thigh_R.rotation_mode = "XYZ"
    pose_thigh_R.rotation_euler = (0, 0, m.radians(3))
    pose_thigh_R.rotation_mode = "QUATERNION"
    pose_foot_R = rig.pose.bones["foot.R"]
    pose_foot_R.rotation_mode = "XYZ"
    pose_foot_R.rotation_euler = (0, 0, m.radians(4))
    pose_foot_R.rotation_mode = "QUATERNION"
    pose_thigh_L = rig.pose.bones["thigh.L"]
    pose_thigh_L.rotation_mode = "XYZ"
    pose_thigh_L.rotation_euler = (0, 0, m.radians(-3))
    pose_thigh_L.rotation_mode = "QUATERNION"
    pose_foot_L = rig.pose.bones["foot.L"]
    pose_foot_L.rotation_mode = "XYZ"
    pose_foot_L.rotation_euler = (0, 0, m.radians(-4))
    pose_foot_L.rotation_mode = "QUATERNION"

    # Apply the actual pose to the rest pose
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.armature_apply(selected=False)

    # Change mode to edit mode
    bpy.ops.object.mode_set(mode="EDIT")

    # Get new bone references
    upper_arm_R = rig.data.edit_bones["upper_arm.R"]
    upper_arm_L = rig.data.edit_bones["upper_arm.L"]
    forearm_R = rig.data.edit_bones["forearm.R"]
    forearm_L = rig.data.edit_bones["forearm.L"]
    hand_R = rig.data.edit_bones["hand.R"]
    hand_L = rig.data.edit_bones["hand.L"]

    # Get average upperarm length
    avg_upper_arm_length = (
        bone_data["upper_arm.R"]["median"] + bone_data["upper_arm.L"]["median"]
    ) / 2

    # Set the upperarm bones length based on the keep symmetry parameter
    upper_arm_R_length = (
        avg_upper_arm_length if keep_symmetry else bone_data["upper_arm.R"]["median"]
    )
    upper_arm_L_length = (
        avg_upper_arm_length if keep_symmetry else bone_data["upper_arm.L"]["median"]
    )

    # Move the upper_arm tail in the x axis
    upper_arm_R.tail[0] = upper_arm_R.head[0] - upper_arm_R_length
    upper_arm_L.tail[0] = upper_arm_L.head[0] + upper_arm_L_length

    # Get average forearm length
    avg_forearm_length = (
        bone_data["forearm.R"]["median"] + bone_data["forearm.L"]["median"]
    ) / 2

    # Set the forearm bones length based on the keep symmetry parameter
    forearm_R_length = (
        avg_forearm_length if keep_symmetry else bone_data["forearm.R"]["median"]
    )
    forearm_L_length = (
        avg_forearm_length if keep_symmetry else bone_data["forearm.L"]["median"]
    )

    # Calculate the x axis offset of the current forearm tail x position and the forearm head x position plus the calculated forearm length
    # This is to move the forearm tail and all the hand bones
    forearm_R_tail_x_offset = (forearm_R.head[0] - forearm_R_length) - forearm_R.tail[0]
    forearm_L_tail_x_offset = (forearm_L.head[0] + forearm_L_length) - forearm_L.tail[0]

    # Move forearms tail and its children by the x offset
    forearm_R.tail[0] += forearm_R_tail_x_offset
    for bone_constraint_definition in forearm_R.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[0] += forearm_R_tail_x_offset
            bone_constraint_definition.tail[0] += forearm_R_tail_x_offset
        else:
            bone_constraint_definition.tail[0] += forearm_R_tail_x_offset

    forearm_L.tail[0] += forearm_L_tail_x_offset
    for bone_constraint_definition in forearm_L.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[0] += forearm_L_tail_x_offset
            bone_constraint_definition.tail[0] += forearm_L_tail_x_offset
        else:
            bone_constraint_definition.tail[0] += forearm_L_tail_x_offset

    #############################################################
    ### DEBUG ###
    if False:
        # Add an auxiliary bone to the side of the upperarms and forearms to check their rotation
        upper_arm_R_Rot = rig.data.edit_bones.new("uppe_rarm.R.Rot")
        upper_arm_R_Rot.head = (
            upper_arm_R.head[0] - upper_arm_R_length / 2,
            upper_arm_R.head[1],
            upper_arm_R.head[2],
        )
        upper_arm_R_Rot.tail = (
            upper_arm_R_Rot.head[0],
            upper_arm_R_Rot.head[1],
            upper_arm_R_Rot.head[2] + 0.1,
        )
        upper_arm_R_Rot.parent = upper_arm_R
        upper_arm_R_Rot.use_connect = False
        upper_arm_L_Rot = rig.data.edit_bones.new("uppe_rarm.L.Rot")
        upper_arm_L_Rot.head = (
            upper_arm_L.head[0] + upper_arm_L_length / 2,
            upper_arm_L.head[1],
            upper_arm_L.head[2],
        )
        upper_arm_L_Rot.tail = (
            upper_arm_L_Rot.head[0],
            upper_arm_L_Rot.head[1],
            upper_arm_L_Rot.head[2] + 0.1,
        )
        upper_arm_L_Rot.parent = upper_arm_L
        upper_arm_L_Rot.use_connect = False
        forearm_R_Rot = rig.data.edit_bones.new("uppe_rarm.R.Rot")
        forearm_R_Rot.head = (
            forearm_R.head[0] - forearm_R_length / 2,
            forearm_R.head[1],
            forearm_R.head[2],
        )
        forearm_R_Rot.tail = (
            forearm_R_Rot.head[0],
            forearm_R_Rot.head[1],
            forearm_R_Rot.head[2] + 0.1,
        )
        forearm_R_Rot.parent = forearm_R
        forearm_R_Rot.use_connect = False
        forearm_L_Rot = rig.data.edit_bones.new("uppe_rarm.L.Rot")
        forearm_L_Rot.head = (
            forearm_L.head[0] + forearm_L_length / 2,
            forearm_L.head[1],
            forearm_L.head[2],
        )
        forearm_L_Rot.tail = (
            forearm_L_Rot.head[0],
            forearm_L_Rot.head[1],
            forearm_L_Rot.head[2] + 0.1,
        )
        forearm_L_Rot.parent = forearm_L
        forearm_L_Rot.use_connect = False
    #############################################################

    # Get average hand length
    avg_hand_length = (
        bone_data["hand.R"]["median"] + bone_data["hand.L"]["median"]
    ) / 2

    # Set the forearm bones length based on the keep symmetry parameter
    hand_R_length = avg_hand_length if keep_symmetry else bone_data["hand.R"]["median"]
    hand_L_length = avg_hand_length if keep_symmetry else bone_data["hand.L"]["median"]

    # Move hands tail to match the average length
    hand_R.tail[0] = hand_R.head[0] - hand_R_length
    hand_L.tail[0] = hand_L.head[0] + hand_L_length

    ### Adjust the position of the neck, head and face bones ###
    spine_001 = rig.data.edit_bones["spine.001"]
    spine_004 = rig.data.edit_bones["spine.004"]
    nose = rig.data.edit_bones["nose"]
    nose_001 = rig.data.edit_bones["nose.001"]

    # Set spine.004 bone head position equal to the spine.001 tail
    spine_004.head = (spine_001.tail[0], spine_001.tail[1], spine_001.tail[2])

    # Change spine.004 tail position values
    spine_004.tail = (
        spine_004.head[0],
        spine_004.head[1],
        spine_004.head[2] + bone_data["neck"]["median"],
    )

    # Change the parent of the face bone for the spine.004 bone
    face = rig.data.edit_bones["face"]
    face.parent = spine_004
    face.use_connect = False

    # Remove spine.005 and spine.006 bones
    rig.data.edit_bones.remove(rig.data.edit_bones["spine.005"])
    rig.data.edit_bones.remove(rig.data.edit_bones["spine.006"])

    # Calculate the y and z offset of the nose.001 bone tail using the imaginary head_nose bone. Assume a 18º of declination angle
    nose_y_offset = (
        -bone_data["head_nose"]["median"] * m.cos(m.radians(18)) - nose_001.tail[1]
    )
    nose_z_offset = (
        spine_004.tail[2] - bone_data["head_nose"]["median"] * m.sin(m.radians(18))
    ) - nose_001.tail[2]

    # Move the face bone on the z axis using the calculated offset
    face.head[2] += nose_z_offset
    face.tail[2] += nose_z_offset

    # Move on the y and z axis the children bones from the face bone using the calculated offsets
    for bone_constraint_definition in face.children_recursive:
        if not bone_constraint_definition.use_connect:
            bone_constraint_definition.head[1] += nose_y_offset
            bone_constraint_definition.tail[1] += nose_y_offset
            bone_constraint_definition.head[2] += nose_z_offset
            bone_constraint_definition.tail[2] += nose_z_offset
        else:
            bone_constraint_definition.tail[1] += nose_y_offset
            bone_constraint_definition.tail[2] += nose_z_offset

    # Move the face bone head to align it horizontally
    face.head[1] = spine_004.tail[1]
    face.head[2] = face.tail[2]
    face.tail[1] = face.head[1] - (
        bone_data["head_nose"]["median"] * m.cos(m.radians(18)) / 2
    )

    # Rename spine.004 to neck
    rig.data.edit_bones["spine.004"].name = "neck"

    # Rotate the spine and neck bones to complete the TPOSE
    bpy.ops.object.mode_set(mode="POSE")

    pose_spine = rig.pose.bones["spine"]
    pose_spine.rotation_mode = "XYZ"
    pose_spine.rotation_euler = (m.radians(3), 0, 0)
    pose_spine.rotation_mode = "QUATERNION"
    pose_spine_001 = rig.pose.bones["spine.001"]
    pose_spine_001.rotation_mode = "XYZ"
    pose_spine_001.rotation_euler = (m.radians(-10), 0, 0)
    pose_spine_001.rotation_mode = "QUATERNION"
    pose_neck = rig.pose.bones["neck"]
    pose_neck.rotation_mode = "XYZ"
    pose_neck.rotation_euler = (m.radians(6), 0, 0)
    pose_neck.rotation_mode = "QUATERNION"

    # Apply the actual pose to the rest pose
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.armature_apply(selected=False)

    # Adjust the fingers

    # Change mode to edit mode
    bpy.ops.object.mode_set(mode="EDIT")

    # Get new bone references
    hand_R = rig.data.edit_bones["hand.R"]
    hand_L = rig.data.edit_bones["hand.L"]
    palm_01_R = rig.data.edit_bones["palm.01.R"]
    palm_01_L = rig.data.edit_bones["palm.01.L"]
    palm_02_R = rig.data.edit_bones["palm.02.R"]
    palm_02_L = rig.data.edit_bones["palm.02.L"]
    palm_03_R = rig.data.edit_bones["palm.03.R"]
    palm_03_L = rig.data.edit_bones["palm.03.L"]
    palm_04_R = rig.data.edit_bones["palm.04.R"]
    palm_04_L = rig.data.edit_bones["palm.04.L"]
    thumb_01_R = rig.data.edit_bones["thumb.01.R"]
    thumb_01_L = rig.data.edit_bones["thumb.01.L"]
    thumb_02_R = rig.data.edit_bones["thumb.02.R"]
    thumb_02_L = rig.data.edit_bones["thumb.02.L"]
    thumb_03_R = rig.data.edit_bones["thumb.03.R"]
    thumb_03_L = rig.data.edit_bones["thumb.03.L"]
    f_index_01_R = rig.data.edit_bones["f_index.01.R"]
    f_index_01_L = rig.data.edit_bones["f_index.01.L"]
    f_index_02_R = rig.data.edit_bones["f_index.02.R"]
    f_index_02_L = rig.data.edit_bones["f_index.02.L"]
    f_index_03_R = rig.data.edit_bones["f_index.03.R"]
    f_index_03_L = rig.data.edit_bones["f_index.03.L"]
    f_middle_01_R = rig.data.edit_bones["f_middle.01.R"]
    f_middle_01_L = rig.data.edit_bones["f_middle.01.L"]
    f_middle_02_R = rig.data.edit_bones["f_middle.02.R"]
    f_middle_02_L = rig.data.edit_bones["f_middle.02.L"]
    f_middle_03_R = rig.data.edit_bones["f_middle.03.R"]
    f_middle_03_L = rig.data.edit_bones["f_middle.03.L"]
    f_ring_01_R = rig.data.edit_bones["f_ring.01.R"]
    f_ring_01_L = rig.data.edit_bones["f_ring.01.L"]
    f_ring_02_R = rig.data.edit_bones["f_ring.02.R"]
    f_ring_02_L = rig.data.edit_bones["f_ring.02.L"]
    f_ring_03_R = rig.data.edit_bones["f_ring.03.R"]
    f_ring_03_L = rig.data.edit_bones["f_ring.03.L"]
    f_pinky_01_R = rig.data.edit_bones["f_pinky.01.R"]
    f_pinky_01_L = rig.data.edit_bones["f_pinky.01.L"]
    f_pinky_02_R = rig.data.edit_bones["f_pinky.02.R"]
    f_pinky_02_L = rig.data.edit_bones["f_pinky.02.L"]
    f_pinky_03_R = rig.data.edit_bones["f_pinky.03.R"]
    f_pinky_03_L = rig.data.edit_bones["f_pinky.03.L"]

    # Add the thumb carpals
    thumb_carpal_R = rig.data.edit_bones.new("thumb.carpal.R")
    thumb_carpal_R.head = hand_R.head
    thumb_carpal_R.tail = thumb_carpal_R.head + mathutils.Vector(
        [0, -bone_data["thumb.carpal.R"]["median"], 0]
    )
    thumb_carpal_L = rig.data.edit_bones.new("thumb.carpal.L")
    thumb_carpal_L.head = hand_L.head
    thumb_carpal_L.tail = thumb_carpal_L.head + mathutils.Vector(
        [0, -bone_data["thumb.carpal.L"]["median"], 0]
    )

    # Asign the parent to thumb carpals
    thumb_carpal_R.parent = hand_R
    thumb_carpal_R.use_connect = False
    thumb_carpal_L.parent = hand_L
    thumb_carpal_L.use_connect = False

    # Change the parent of thumb.01 to thumb.carpal
    thumb_01_R.parent = thumb_carpal_R
    thumb_01_L.parent = thumb_carpal_L

    # Create a palm bones list and phalanges dictionary to continue the finger adjustment
    palm_bones = [
        thumb_carpal_R,
        thumb_carpal_L,
        palm_01_R,
        palm_01_L,
        palm_02_R,
        palm_02_L,
        palm_03_R,
        palm_03_L,
        palm_04_R,
        palm_04_L,
    ]
    phalanges = {
        "thumb.carpal.R": [thumb_01_R, thumb_02_R, thumb_03_R],
        "thumb.carpal.L": [thumb_01_L, thumb_02_L, thumb_03_L],
        "palm.01.R": [f_index_01_R, f_index_02_R, f_index_03_R],
        "palm.01.L": [f_index_01_L, f_index_02_L, f_index_03_L],
        "palm.02.R": [f_middle_01_R, f_middle_02_R, f_middle_03_R],
        "palm.02.L": [f_middle_01_L, f_middle_02_L, f_middle_03_L],
        "palm.03.R": [f_ring_01_R, f_ring_02_R, f_ring_03_R],
        "palm.03.L": [f_ring_01_L, f_ring_02_L, f_ring_03_L],
        "palm.04.R": [f_pinky_01_R, f_pinky_02_R, f_pinky_03_R],
        "palm.04.L": [f_pinky_01_L, f_pinky_02_L, f_pinky_03_L],
    }

    # Iterate through the palm bones to adjust several properties
    for palm_bone in palm_bones:
        # Change the first phalange connect setting to True
        phalanges[palm_bone.name][0].use_connect = True
        # Move the head of the metacarpal bones to match the hand bone head
        palm_bone.head = palm_bone.parent.head
        # Move the tail of the metacarpal bones so they are aligned horizontally
        palm_bone.tail[2] = palm_bone.head[2]
        # Change metacarpal bones lengths
        palm_bone.length = bone_data[palm_bone.name]["median"]

    # Align the phalanges to the x axis (set bones head and tail y position equal to yz position of metacarpals bone tail)
    for palm_bone in palm_bones:
        for phalange in phalanges[palm_bone.name]:
            phalange.head = phalange.parent.tail
            # Calculate the sign to multiply the length of the phalange
            length_sign = -1 if ".R" in phalange.name else 1
            # Set the length by moving the bone tail along the x axis. Using this instead of just setting bone.length because that causes some bone inversions
            phalange.tail = (
                phalange.head[0] + length_sign * bone_data[phalange.name]["median"],
                phalange.head[1],
                phalange.head[2],
            )
            # Reset the phalange bone roll to 0
            phalange.roll = 0

    # Rotate the thumb bones to form a natural pose
    bpy.ops.object.mode_set(mode="POSE")

    pose_thumb_carpal_R = rig.pose.bones["thumb.carpal.R"]
    pose_thumb_carpal_R.rotation_mode = "XYZ"
    pose_thumb_carpal_R.rotation_euler = (
        m.radians(-28.048091),
        m.radians(7.536737),
        m.radians(-40.142189),
    )
    pose_thumb_carpal_R.rotation_mode = "QUATERNION"
    pose_thumb_01_R = rig.pose.bones["thumb.01.R"]
    pose_thumb_01_R.rotation_mode = "XYZ"
    # pose_thumb_01_R.rotation_euler      = (m.radians(20), m.radians(0), m.radians(80))
    pose_thumb_01_R.rotation_euler = (m.radians(0), m.radians(0), m.radians(90))
    pose_thumb_01_R.rotation_mode = "QUATERNION"
    # pose_thumb_02_R                     = rig.pose.bones['thumb.02.R']
    # pose_thumb_02_R.rotation_mode       = 'XYZ'
    # pose_thumb_02_R.rotation_euler      = (m.radians(0), m.radians(0), m.radians(-25))
    # pose_thumb_02_R.rotation_mode       = 'QUATERNION'
    # pose_thumb_03_R                     = rig.pose.bones['thumb.03.R']
    # pose_thumb_03_R.rotation_mode       = 'XYZ'
    # pose_thumb_03_R.rotation_euler      = (m.radians(0), m.radians(0), m.radians(-10))
    # pose_thumb_03_R.rotation_mode       = 'QUATERNION'
    pose_thumb_carpal_L = rig.pose.bones["thumb.carpal.L"]
    pose_thumb_carpal_L.rotation_mode = "XYZ"
    pose_thumb_carpal_L.rotation_euler = (
        m.radians(-28.048091),
        m.radians(-7.536737),
        m.radians(40.142189),
    )
    pose_thumb_carpal_L.rotation_mode = "QUATERNION"
    pose_thumb_01_L = rig.pose.bones["thumb.01.L"]
    pose_thumb_01_L.rotation_mode = "XYZ"
    # pose_thumb_01_L.rotation_euler      = (m.radians(20), m.radians(0), m.radians(-80))
    pose_thumb_01_L.rotation_euler = (m.radians(0), m.radians(0), m.radians(-90))
    pose_thumb_01_L.rotation_mode = "QUATERNION"
    # pose_thumb_02_L                     = rig.pose.bones['thumb.02.L']
    # pose_thumb_02_L.rotation_mode       = 'XYZ'
    # pose_thumb_02_L.rotation_euler      = (m.radians(0), m.radians(0), m.radians(25))
    # pose_thumb_02_L.rotation_mode       = 'QUATERNION'
    # pose_thumb_03_L                     = rig.pose.bones['thumb.03.L']
    # pose_thumb_03_L.rotation_mode       = 'XYZ'
    # pose_thumb_03_L.rotation_euler      = (m.radians(0), m.radians(0), m.radians(10))
    # pose_thumb_03_L.rotation_mode       = 'QUATERNION'

    # Rotate the forearms on the z axis to bend the elbows a little bit and avoid incorrect rotations
    pose_forearm_R = rig.pose.bones["forearm.R"]
    pose_forearm_R.rotation_mode = "XYZ"
    pose_forearm_R.rotation_euler = (m.radians(1), m.radians(0), m.radians(0))
    pose_forearm_R.rotation_mode = "QUATERNION"
    pose_forearm_L = rig.pose.bones["forearm.L"]
    pose_forearm_L.rotation_mode = "XYZ"
    pose_forearm_L.rotation_euler = (m.radians(1), m.radians(0), m.radians(0))
    pose_forearm_L.rotation_mode = "QUATERNION"

    # Apply the actual pose to the rest pose
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.armature_apply(selected=False)

    return rig


def add_rig_by_bone(
    bone_data: Dict[str, Dict[str, float]],
    armature: Dict[str, ArmatureBoneInfo] = ArmatureType.FREEMOCAP,
    pose: Dict[str, PoseElement] = PoseType.FREEMOCAP_TPOSE,
    add_ik_constraints: bool = False,
) -> bpy.types.Object:
    print("Adding rig to scene bone by bone...")
    if armature == ArmatureType.UE_METAHUMAN_SIMPLE:
        armature_name = UE_METAHUMAN_SIMPLE_ARMATURE
    elif armature == ArmatureType.FREEMOCAP:
        armature_name = FREEMOCAP_ARMATURE
    else:
        raise ValueError("Invalid armature name")

    # Get rig height as the sum of the major bones length in a standing position. Assume foot declination angle of 23º
    avg_ankle_projection_length = (
        m.sin(m.radians(23)) * bone_data["foot.R"]["median"]
        + m.sin(m.radians(23)) * bone_data["foot.L"]["median"]
    ) / 2
    avg_shin_length = (
        bone_data["shin.R"]["median"] + bone_data["shin.L"]["median"]
    ) / 2
    avg_thigh_length = (
        bone_data["thigh.R"]["median"] + bone_data["thigh.L"]["median"]
    ) / 2

    # Add the armature
    bpy.ops.object.armature_add(
        enter_editmode=False,
        align="WORLD",
        location=(0, 0, 0),
    )

    # Rename the armature
    bpy.data.armatures[0].name = "root"
    # Get reference to armature
    rig = bpy.data.objects["Armature"]
    # Rename the rig object to pelvis
    rig.name = "root"
    # Get reference to the renamed armature
    rig = bpy.data.objects["root"]

    # Change to edit mode
    bpy.ops.object.mode_set(mode="EDIT")

    # Remove the default bone
    rig.data.edit_bones.remove(rig.data.edit_bones["Bone"])

    # Get the inverse bone_map_dict
    inv_bone_name_map = {
        value: key for key, value in bone_name_map[armature_name].items()
    }

    # Iterate over the armature dictionary
    for bone in armature:

        # Get the reference to the parent of the bone if its not root
        parent_name = armature[bone].parent_bone
        if parent_name != "root":
            parent_bone = rig.data.edit_bones[parent_name]

        # Add the new bone
        rig_bone = rig.data.edit_bones.new(bone)

        # Set the bone head position
        if bone in ("pelvis"):
            rig_bone.head = mathutils.Vector(
                [
                    0,
                    0,
                    avg_ankle_projection_length + avg_shin_length + avg_thigh_length,
                ]
            )
        else:
            # Set the bone position relative to its parent
            if armature[bone].parent_position == "head":
                rig_bone.head = parent_bone.head
            elif armature[bone].parent_position == "tail":
                rig_bone.head = parent_bone.tail

        # Get the bone vector
        if inv_bone_name_map[bone] not in bone_data:
            bone_vector = mathutils.Vector(
                [0, 0, armature[bone].default_length]
            )
        else:
            bone_vector = mathutils.Vector(
                [0, 0, bone_data[inv_bone_name_map[bone]]["median"]]
            )

        # Get the rotation matrix
        rotation_matrix = mathutils.Euler(
            mathutils.Vector(pose[bone].rotation),
            "XYZ",
        ).to_matrix()

        # Rotate the bone vector
        rig_bone.tail = rig_bone.head + rotation_matrix @ bone_vector

        # Assign the roll to the bone
        rig_bone.roll = pose[bone].roll

        # Parent the bone if its parent exists
        if parent_name != "root":
            rig_bone.parent = parent_bone
            rig_bone.use_connect = armature[bone].connected

    # Special armature conditions
    if armature_name == UE_METAHUMAN_SIMPLE_ARMATURE:
        # Change parents of thigh bones
        rig.data.edit_bones["thigh_r"].use_connect = False
        rig.data.edit_bones["thigh_l"].use_connect = False
        rig.data.edit_bones["thigh_r"].parent = rig.data.edit_bones["pelvis"]
        rig.data.edit_bones["thigh_l"].parent = rig.data.edit_bones["pelvis"]

    # Add the ik bones if specified
    if add_ik_constraints:
        for ik_control in ik_control_bones:
            ik_bone = rig.data.edit_bones.new(ik_control)
            ik_bone.head = rig.data.edit_bones[
                bone_name_map[armature_name][
                    ik_control_bones[ik_control].controlled_bone
                ]
            ].head
            ik_bone.tail = ik_bone.head + mathutils.Vector(
                ik_control_bones[ik_control].tail_relative_position
            )
        for ik_pole in ik_pole_bones:
            ik_bone = rig.data.edit_bones.new(ik_pole)
            ik_bone.head = ik_pole_bones[ik_pole].head_position
            ik_bone.tail = ik_pole_bones[ik_pole].tail_position

    return rig


def add_constraints(
    rig: bpy.types.Object,
    add_fingers_constraints: bool,
    parent_object: bpy.types.Object,
    armature: Dict[str, ArmatureBoneInfo] = ArmatureType.FREEMOCAP,
    pose: Dict[str, PoseElement] = PoseType.FREEMOCAP_TPOSE,
    use_limit_rotation: bool = False,
) -> None:
    if armature == ArmatureType.UE_METAHUMAN_SIMPLE:
        armature_name = UE_METAHUMAN_SIMPLE_ARMATURE
    elif armature == ArmatureType.FREEMOCAP:
        armature_name = FREEMOCAP_ARMATURE
    else:
        raise ValueError("Invalid armature name")
    
    if pose == PoseType.FREEMOCAP_TPOSE:
        pose_name = FREEMOCAP_TPOSE
    elif pose == PoseType.FREEMOCAP_APOSE:
        pose_name = FREEMOCAP_APOSE
    elif pose == PoseType.UE_METAHUMAN_DEFAULT:
        pose_name = UE_METAHUMAN_DEFAULT
    elif pose == PoseType.UE_METAHUMAN_TPOSE:
        pose_name = UE_METAHUMAN_TPOSE
    else:
        raise ValueError("Invalid pose name")

    print("Adding bone constraints...")
    # TODO: getting key error in this function with Failed to add rig: 'bpy_prop_collection[key]: key "pelvis.R" not found'
    # Change to pose mode
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    #
    # # Define the hand bones damped track target as the hand middle empty if they were already added
    # try:
    #     right_hand_middle_name = bpy.data.objects['right_hand_middle'].name
    #     # Right Hand Middle Empty exists. Use hand middle as target
    #     hand_damped_track_target = 'hand_middle'
    # except:
    #     # Hand middle empties do not exist. Use hand_index as target
    #     hand_damped_track_target = 'index'

    # Create each constraint
    for (
        bone_name,
        constraint_definitions,
    ) in ALL_BONES_CONSTRAINT_DEFINITIONS.items():
        # If pose bone does not exist, skip it
        if bone_name not in rig.pose.bones:
            continue
        
        if not isinstance(constraint_definitions, list):
            raise Exception(f"Constraint definitions for {bone_name} must be a list")

        # If it is a finger bone amd add_fingers_constraints is False continue with the next bone
        if (
            not add_fingers_constraints
            and len(
                [
                    finger_part
                    for finger_part in [
                        "palm",
                        "thumb",
                        "index",
                        "middle",
                        "ring",
                        "pinky",
                    ]
                    if finger_part
                    in constraint_definitions
                ]
            )
            > 0
        ):
            continue

        for constraint in constraint_definitions:
            # if "target" in constraint.keys():
            #     base_target_name = constraint["target"]
            #     actual_target_name = get_actual_empty_target_name(empty_names = empty_names,
            #                                                       base_target_name = base_target_name)
            #     constraint["target"] = actual_target_name
            appended_number_string = get_appended_number(parent_object.name)
            if appended_number_string is not None:
                if hasattr(constraint, "target"):
                    constraint.target = constraint.target + appended_number_string
            # Add new constraint determined by type
            if not use_limit_rotation and constraint.type == ConstraintType.LIMIT_ROTATION:
                continue
            else:
                try:
                    bone_constraint = rig.pose.bones[bone_name_map[armature_name][bone_name]].constraints.new(
                        constraint.type.value
                    )
                except:
                    print(f"Failed to add rig: {bone_name} constraint {constraint.type}")
                    continue

                # Define aditional parameters based on the type of constraint
            if isinstance(constraint, LimitRotationConstraint):
                bone_constraint.use_limit_x = constraint.use_limit_x
                bone_constraint.min_x = m.radians(constraint.min_x)
                bone_constraint.max_x = m.radians(constraint.max_x)
                bone_constraint.use_limit_y = constraint.use_limit_y
                bone_constraint.min_y = m.radians(constraint.min_y)
                bone_constraint.max_y = m.radians(constraint.max_y)
                bone_constraint.use_limit_z = constraint.use_limit_z
                bone_constraint.min_z = m.radians(constraint.min_z)
                bone_constraint.max_z = m.radians(constraint.max_z)
                bone_constraint.owner_space = constraint.owner_space.value
            elif isinstance(constraint, CopyLocationConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
            elif isinstance(constraint, LockedTrackConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
                bone_constraint.track_axis = constraint.track_axis[pose_name].value
                bone_constraint.lock_axis = constraint.lock_axis[pose_name].value
                bone_constraint.influence = constraint.influence
            elif isinstance(constraint, DampedTrackConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
                bone_constraint.track_axis = constraint.track_axis.value
            elif isinstance(constraint, IKConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
                bone_constraint.pole_target = bpy.data.objects[
                    constraint.pole_target
                ]
                bone_constraint.chain_count = constraint.chain_count
                bone_constraint.pole_angle = constraint.pole_angle


def ensure_rigify() -> None:
    _, rigify_enabled = addon_utils.check("rigify")

    if not rigify_enabled:
        try:
            print("Rigify not found - enabling Rigify addon...")
            addon_utils.enable(
                "rigify", default_set=True, persistent=True, handle_error=print
            )
        except Exception as e:
            print(f"Error enabling Rigify addon - \n\n{e}")
            raise e

    _, rigify_enabled = addon_utils.check("rigify")

    if not rigify_enabled:
        raise Exception(
            "Rigify not enabled, please enable it in your blender preferences and then close blender before retrying"
        )


def get_appended_number(rig_name: str) -> Optional[str]:
    pattern = r"\.0[0-9]{2}$"
    match = re.search(pattern, rig_name)
    return match.group() if match else None


def get_actual_empty_target_name(empty_names: List[str], base_target_name: str) -> str:
    """
    Get the actual empty target name based on the constraint target name,
    this is mostly to give us the ability to load multiple recorings, because
    blender will append `.001`, `.002`  the names of emtpies of the 2nd, 3rd, etc to avoid name collisions

    So basically, if the base_target name is `hips_center` this will look for empties named `hips_center`,
      `hips_center.001`, `hips_center.002`, etc in the provided `empty_names` list and return that
    """

    actual_target_name = None
    for empty_name in empty_names:
        if base_target_name in empty_name:
            actual_target_name = empty_name
            break

    if actual_target_name is None:
        raise ValueError(f"Could not find empty target for {base_target_name}")

    return actual_target_name
