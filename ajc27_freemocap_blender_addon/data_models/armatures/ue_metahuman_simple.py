from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import (
    ArmatureBoneInfo,
)

armature_ue_metahuman_simple = {
    "pelvis": ArmatureBoneInfo(
        parent_bone="root",
        connected=False,
        parent_position="head",
        default_length=0.05,
    ),
    "pelvis_r": ArmatureBoneInfo(
        parent_bone="pelvis",
        connected=False,
        parent_position="head",
    ),
    "pelvis_l": ArmatureBoneInfo(
        parent_bone="pelvis",
        connected=False,
        parent_position="head",
    ),
    "spine_01": ArmatureBoneInfo(
        parent_bone="pelvis",
        connected=False,
        parent_position="head",
    ),
    "spine_04": ArmatureBoneInfo(
        parent_bone="spine_01",
    ),
    "neck_01": ArmatureBoneInfo(
        parent_bone="spine_04",
    ),
    "face": ArmatureBoneInfo(
        parent_bone="neck_01",
        default_length=0.1,
    ),
    "clavicle_r": ArmatureBoneInfo(
        parent_bone="spine_04",
    ),
    "clavicle_l": ArmatureBoneInfo(
        parent_bone="spine_04",
    ),
    "upperarm_r": ArmatureBoneInfo(
        parent_bone="clavicle_r",
    ),
    "upperarm_l": ArmatureBoneInfo(
        parent_bone="clavicle_l",
    ),
    "lowerarm_r": ArmatureBoneInfo(
        parent_bone="upperarm_r",
    ),
    "lowerarm_l": ArmatureBoneInfo(
        parent_bone="upperarm_l",
    ),
    "hand_r": ArmatureBoneInfo(
        parent_bone="lowerarm_r",
    ),
    "hand_l": ArmatureBoneInfo(
        parent_bone="lowerarm_l",
    ),
    "thumb_metacarpal_r": ArmatureBoneInfo(
        parent_bone="hand_r",
        connected=False,
        parent_position="head",
    ),
    "thumb_metacarpal_l": ArmatureBoneInfo(
        parent_bone="hand_l",
        connected=False,
        parent_position="head",
    ),
    "thumb_01_r": ArmatureBoneInfo(
        parent_bone="thumb_metacarpal_r",
    ),
    "thumb_01_l": ArmatureBoneInfo(
        parent_bone="thumb_metacarpal_l",
    ),
    "thumb_02_r": ArmatureBoneInfo(
        parent_bone="thumb_01_r",
    ),
    "thumb_02_l": ArmatureBoneInfo(
        parent_bone="thumb_01_l",
    ),
    "thumb_03_r": ArmatureBoneInfo(
        parent_bone="thumb_02_r",
    ),
    "thumb_03_l": ArmatureBoneInfo(
        parent_bone="thumb_02_l",
    ),
    "index_metacarpal_r": ArmatureBoneInfo(
        parent_bone="hand_r",
        connected=False,
        parent_position="head",
    ),
    "index_metacarpal_l": ArmatureBoneInfo(
        parent_bone="hand_l",
        connected=False,
        parent_position="head",
    ),
    "index_01_r": ArmatureBoneInfo(
        parent_bone="index_metacarpal_r",
    ),
    "index_01_l": ArmatureBoneInfo(
        parent_bone="index_metacarpal_l",
    ),
    "index_02_r": ArmatureBoneInfo(
        parent_bone="index_01_r",
    ),
    "index_02_l": ArmatureBoneInfo(
        parent_bone="index_01_l",
    ),
    "index_03_r": ArmatureBoneInfo(
        parent_bone="index_02_r",
    ),
    "index_03_l": ArmatureBoneInfo(
        parent_bone="index_02_l",
    ),
    "middle_metacarpal_r": ArmatureBoneInfo(
        parent_bone="hand_r",
        connected=False,
        parent_position="head",
    ),
    "middle_metacarpal_l": ArmatureBoneInfo(
        parent_bone="hand_l",
        connected=False,
        parent_position="head",
    ),
    "middle_01_r": ArmatureBoneInfo(
        parent_bone="middle_metacarpal_r",
    ),
    "middle_01_l": ArmatureBoneInfo(
        parent_bone="middle_metacarpal_l",
    ),
    "middle_02_r": ArmatureBoneInfo(
        parent_bone="middle_01_r",
    ),
    "middle_02_l": ArmatureBoneInfo(
        parent_bone="middle_01_l",
    ),
    "middle_03_r": ArmatureBoneInfo(
        parent_bone="middle_02_r",
    ),
    "middle_03_l": ArmatureBoneInfo(
        parent_bone="middle_02_l",
    ),
    "ring_metacarpal_r": ArmatureBoneInfo(
        parent_bone="hand_r",
        connected=False,
        parent_position="head",
    ),
    "ring_metacarpal_l": ArmatureBoneInfo(
        parent_bone="hand_l",
        connected=False,
        parent_position="head",
    ),
    "ring_01_r": ArmatureBoneInfo(
        parent_bone="ring_metacarpal_r",
    ),
    "ring_01_l": ArmatureBoneInfo(
        parent_bone="ring_metacarpal_l",
    ),
    "ring_02_r": ArmatureBoneInfo(
        parent_bone="ring_01_r",
    ),
    "ring_02_l": ArmatureBoneInfo(
        parent_bone="ring_01_l",
    ),
    "ring_03_r": ArmatureBoneInfo(
        parent_bone="ring_02_r",
    ),
    "ring_03_l": ArmatureBoneInfo(
        parent_bone="ring_02_l",
    ),
    "pinky_metacarpal_r": ArmatureBoneInfo(
        parent_bone="hand_r",
        connected=False,
        parent_position="head",
    ),
    "pinky_metacarpal_l": ArmatureBoneInfo(
        parent_bone="hand_l",
        connected=False,
        parent_position="head",
    ),
    "pinky_01_r": ArmatureBoneInfo(
        parent_bone="pinky_metacarpal_r",
    ),
    "pinky_01_l": ArmatureBoneInfo(
        parent_bone="pinky_metacarpal_l",
    ),
    "pinky_02_r": ArmatureBoneInfo(
        parent_bone="pinky_01_r",
    ),
    "pinky_02_l": ArmatureBoneInfo(
        parent_bone="pinky_01_l",
    ),
    "pinky_03_r": ArmatureBoneInfo(
        parent_bone="pinky_02_r",
    ),
    "pinky_03_l": ArmatureBoneInfo(
        parent_bone="pinky_02_l",
    ),
    "thigh_r": ArmatureBoneInfo(
        parent_bone="pelvis_r",
    ),
    "thigh_l": ArmatureBoneInfo(
        parent_bone="pelvis_l",
    ),
    "calf_r": ArmatureBoneInfo(
        parent_bone="thigh_r",
    ),
    "calf_l": ArmatureBoneInfo(
        parent_bone="thigh_l",
    ),
    "foot_r": ArmatureBoneInfo(
        parent_bone="calf_r",
    ),
    "foot_l": ArmatureBoneInfo(
        parent_bone="calf_l",
    ),
    "heel_r": ArmatureBoneInfo(
        parent_bone="calf_r",
    ),
    "heel_l": ArmatureBoneInfo(
        parent_bone="calf_l",
    ),
}
