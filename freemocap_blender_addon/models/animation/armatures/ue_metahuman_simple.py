from freemocap_blender_addon.models.animation.armatures.armature_bone_info import (
    ArmatureBoneDefinition,
)

armature_ue_metahuman_simple = {
    "pelvis": ArmatureBoneDefinition(
        parent_bone_name="root",
        is_connected=False,
        parent_position="head",
        length=0.05,
    ),
    "pelvis_r": ArmatureBoneDefinition(
        parent_bone_name="pelvis",
        is_connected=False,
        parent_position="head",
    ),
    "pelvis_l": ArmatureBoneDefinition(
        parent_bone_name="pelvis",
        is_connected=False,
        parent_position="head",
    ),
    "spine_01": ArmatureBoneDefinition(
        parent_bone_name="pelvis",
        is_connected=False,
        parent_position="head",
    ),
    "spine_04": ArmatureBoneDefinition(
        parent_bone_name="spine_01",
    ),
    "neck_01": ArmatureBoneDefinition(
        parent_bone_name="spine_04",
    ),
    "face": ArmatureBoneDefinition(
        parent_bone_name="neck_01",
        length=0.1,
    ),
    "clavicle_r": ArmatureBoneDefinition(
        parent_bone_name="spine_04",
    ),
    "clavicle_l": ArmatureBoneDefinition(
        parent_bone_name="spine_04",
    ),
    "upperarm_r": ArmatureBoneDefinition(
        parent_bone_name="clavicle_r",
    ),
    "upperarm_l": ArmatureBoneDefinition(
        parent_bone_name="clavicle_l",
    ),
    "lowerarm_r": ArmatureBoneDefinition(
        parent_bone_name="upperarm_r",
    ),
    "lowerarm_l": ArmatureBoneDefinition(
        parent_bone_name="upperarm_l",
    ),
    "hand_r": ArmatureBoneDefinition(
        parent_bone_name="lowerarm_r",
    ),
    "hand_l": ArmatureBoneDefinition(
        parent_bone_name="lowerarm_l",
    ),
    "thumb_metacarpal_r": ArmatureBoneDefinition(
        parent_bone_name="hand_r",
        is_connected=False,
        parent_position="head",
    ),
    "thumb_metacarpal_l": ArmatureBoneDefinition(
        parent_bone_name="hand_l",
        is_connected=False,
        parent_position="head",
    ),
    "thumb_01_r": ArmatureBoneDefinition(
        parent_bone_name="thumb_metacarpal_r",
    ),
    "thumb_01_l": ArmatureBoneDefinition(
        parent_bone_name="thumb_metacarpal_l",
    ),
    "thumb_02_r": ArmatureBoneDefinition(
        parent_bone_name="thumb_01_r",
    ),
    "thumb_02_l": ArmatureBoneDefinition(
        parent_bone_name="thumb_01_l",
    ),
    "thumb_03_r": ArmatureBoneDefinition(
        parent_bone_name="thumb_02_r",
    ),
    "thumb_03_l": ArmatureBoneDefinition(
        parent_bone_name="thumb_02_l",
    ),
    "index_metacarpal_r": ArmatureBoneDefinition(
        parent_bone_name="hand_r",
        is_connected=False,
        parent_position="head",
    ),
    "index_metacarpal_l": ArmatureBoneDefinition(
        parent_bone_name="hand_l",
        is_connected=False,
        parent_position="head",
    ),
    "index_01_r": ArmatureBoneDefinition(
        parent_bone_name="index_metacarpal_r",
    ),
    "index_01_l": ArmatureBoneDefinition(
        parent_bone_name="index_metacarpal_l",
    ),
    "index_02_r": ArmatureBoneDefinition(
        parent_bone_name="index_01_r",
    ),
    "index_02_l": ArmatureBoneDefinition(
        parent_bone_name="index_01_l",
    ),
    "index_03_r": ArmatureBoneDefinition(
        parent_bone_name="index_02_r",
    ),
    "index_03_l": ArmatureBoneDefinition(
        parent_bone_name="index_02_l",
    ),
    "middle_metacarpal_r": ArmatureBoneDefinition(
        parent_bone_name="hand_r",
        is_connected=False,
        parent_position="head",
    ),
    "middle_metacarpal_l": ArmatureBoneDefinition(
        parent_bone_name="hand_l",
        is_connected=False,
        parent_position="head",
    ),
    "middle_01_r": ArmatureBoneDefinition(
        parent_bone_name="middle_metacarpal_r",
    ),
    "middle_01_l": ArmatureBoneDefinition(
        parent_bone_name="middle_metacarpal_l",
    ),
    "middle_02_r": ArmatureBoneDefinition(
        parent_bone_name="middle_01_r",
    ),
    "middle_02_l": ArmatureBoneDefinition(
        parent_bone_name="middle_01_l",
    ),
    "middle_03_r": ArmatureBoneDefinition(
        parent_bone_name="middle_02_r",
    ),
    "middle_03_l": ArmatureBoneDefinition(
        parent_bone_name="middle_02_l",
    ),
    "ring_metacarpal_r": ArmatureBoneDefinition(
        parent_bone_name="hand_r",
        is_connected=False,
        parent_position="head",
    ),
    "ring_metacarpal_l": ArmatureBoneDefinition(
        parent_bone_name="hand_l",
        is_connected=False,
        parent_position="head",
    ),
    "ring_01_r": ArmatureBoneDefinition(
        parent_bone_name="ring_metacarpal_r",
    ),
    "ring_01_l": ArmatureBoneDefinition(
        parent_bone_name="ring_metacarpal_l",
    ),
    "ring_02_r": ArmatureBoneDefinition(
        parent_bone_name="ring_01_r",
    ),
    "ring_02_l": ArmatureBoneDefinition(
        parent_bone_name="ring_01_l",
    ),
    "ring_03_r": ArmatureBoneDefinition(
        parent_bone_name="ring_02_r",
    ),
    "ring_03_l": ArmatureBoneDefinition(
        parent_bone_name="ring_02_l",
    ),
    "pinky_metacarpal_r": ArmatureBoneDefinition(
        parent_bone_name="hand_r",
        is_connected=False,
        parent_position="head",
    ),
    "pinky_metacarpal_l": ArmatureBoneDefinition(
        parent_bone_name="hand_l",
        is_connected=False,
        parent_position="head",
    ),
    "pinky_01_r": ArmatureBoneDefinition(
        parent_bone_name="pinky_metacarpal_r",
    ),
    "pinky_01_l": ArmatureBoneDefinition(
        parent_bone_name="pinky_metacarpal_l",
    ),
    "pinky_02_r": ArmatureBoneDefinition(
        parent_bone_name="pinky_01_r",
    ),
    "pinky_02_l": ArmatureBoneDefinition(
        parent_bone_name="pinky_01_l",
    ),
    "pinky_03_r": ArmatureBoneDefinition(
        parent_bone_name="pinky_02_r",
    ),
    "pinky_03_l": ArmatureBoneDefinition(
        parent_bone_name="pinky_02_l",
    ),
    "thigh_r": ArmatureBoneDefinition(
        parent_bone_name="pelvis_r",
    ),
    "thigh_l": ArmatureBoneDefinition(
        parent_bone_name="pelvis_l",
    ),
    "calf_r": ArmatureBoneDefinition(
        parent_bone_name="thigh_r",
    ),
    "calf_l": ArmatureBoneDefinition(
        parent_bone_name="thigh_l",
    ),
    "foot_r": ArmatureBoneDefinition(
        parent_bone_name="calf_r",
    ),
    "foot_l": ArmatureBoneDefinition(
        parent_bone_name="calf_l",
    ),
    "heel_r": ArmatureBoneDefinition(
        parent_bone_name="calf_r",
    ),
    "heel_l": ArmatureBoneDefinition(
        parent_bone_name="calf_l",
    ),
}
