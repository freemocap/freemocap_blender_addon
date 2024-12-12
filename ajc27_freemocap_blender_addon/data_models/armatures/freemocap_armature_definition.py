from ajc27_freemocap_blender_addon.core_functions.data_models.armatures.root_bone_name import ROOT_BONE_NAME
from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import (
    ArmatureBoneInfo,
)


armature_freemocap = {
    "pelvis": ArmatureBoneInfo(
        parent_bone=ROOT_BONE_NAME,
        connected=False,
        parent_position="head",
        default_length=0.05,
    ),
    "pelvis.R": ArmatureBoneInfo(
        parent_bone="pelvis",
        connected=False,
        parent_position="head",
    ),
    "pelvis.L": ArmatureBoneInfo(
        parent_bone="pelvis",
        connected=False,
        parent_position="head",
    ),
    "spine": ArmatureBoneInfo(
        parent_bone="pelvis",
        connected=False,
        parent_position="head",
    ),
    "spine.001": ArmatureBoneInfo(
        parent_bone="spine",
    ),
    "neck": ArmatureBoneInfo(
        parent_bone="spine.001",
    ),
    "face": ArmatureBoneInfo(
        parent_bone="neck",
        default_length=0.1,
    ),
    "shoulder.R": ArmatureBoneInfo(
        parent_bone="spine.001",
    ),
    "shoulder.L": ArmatureBoneInfo(
        parent_bone="spine.001",
    ),
    "upper_arm.R": ArmatureBoneInfo(
        parent_bone="shoulder.R",
    ),
    "upper_arm.L": ArmatureBoneInfo(
        parent_bone="shoulder.L",
    ),
    "forearm.R": ArmatureBoneInfo(
        parent_bone="upper_arm.R",
    ),
    "forearm.L": ArmatureBoneInfo(
        parent_bone="upper_arm.L",
    ),
    "hand.R": ArmatureBoneInfo(
        parent_bone="forearm.R",
    ),
    "hand.L": ArmatureBoneInfo(
        parent_bone="forearm.L",
    ),
    "thumb.carpal.R": ArmatureBoneInfo(
        parent_bone="hand.R",
        connected=False,
        parent_position="head",
    ),
    "thumb.carpal.L": ArmatureBoneInfo(
        parent_bone="hand.L",
        connected=False,
        parent_position="head",
    ),
    "thumb.01.R": ArmatureBoneInfo(
        parent_bone="thumb.carpal.R",
    ),
    "thumb.01.L": ArmatureBoneInfo(
        parent_bone="thumb.carpal.L",
    ),
    "thumb.02.R": ArmatureBoneInfo(
        parent_bone="thumb.01.R",
    ),
    "thumb.02.L": ArmatureBoneInfo(
        parent_bone="thumb.01.L",
    ),
    "thumb.03.R": ArmatureBoneInfo(
        parent_bone="thumb.02.R",
    ),
    "thumb.03.L": ArmatureBoneInfo(
        parent_bone="thumb.02.L",
    ),
    "palm.01.R": ArmatureBoneInfo(
        parent_bone="hand.R",
        connected=False,
        parent_position="head",
    ),
    "palm.01.L": ArmatureBoneInfo(
        parent_bone="hand.L",
        connected=False,
        parent_position="head",
    ),
    "f_index.01.R": ArmatureBoneInfo(
        parent_bone="palm.01.R",
    ),
    "f_index.01.L": ArmatureBoneInfo(
        parent_bone="palm.01.L",
    ),
    "f_index.02.R": ArmatureBoneInfo(
        parent_bone="f_index.01.R",
    ),
    "f_index.02.L": ArmatureBoneInfo(
        parent_bone="f_index.01.L",
    ),
    "f_index.03.R": ArmatureBoneInfo(
        parent_bone="f_index.02.R",
    ),
    "f_index.03.L": ArmatureBoneInfo(
        parent_bone="f_index.02.L",
    ),
    "palm.02.R": ArmatureBoneInfo(
        parent_bone="hand.R",
        connected=False,
        parent_position="head",
    ),
    "palm.02.L": ArmatureBoneInfo(
        parent_bone="hand.L",
        connected=False,
        parent_position="head",
    ),
    "f_middle.01.R": ArmatureBoneInfo(
        parent_bone="palm.02.R",
    ),
    "f_middle.01.L": ArmatureBoneInfo(
        parent_bone="palm.02.L",
    ),
    "f_middle.02.R": ArmatureBoneInfo(
        parent_bone="f_middle.01.R",
    ),
    "f_middle.02.L": ArmatureBoneInfo(
        parent_bone="f_middle.01.L",
    ),
    "f_middle.03.R": ArmatureBoneInfo(
        parent_bone="f_middle.02.R",
    ),
    "f_middle.03.L": ArmatureBoneInfo(
        parent_bone="f_middle.02.L",
    ),
    "palm.03.R": ArmatureBoneInfo(
        parent_bone="hand.R",
        connected=False,
        parent_position="head",
    ),
    "palm.03.L": ArmatureBoneInfo(
        parent_bone="hand.L",
        connected=False,
        parent_position="head",
    ),
    "f_ring.01.R": ArmatureBoneInfo(
        parent_bone="palm.03.R",
    ),
    "f_ring.01.L": ArmatureBoneInfo(
        parent_bone="palm.03.L",
    ),
    "f_ring.02.R": ArmatureBoneInfo(
        parent_bone="f_ring.01.R",
    ),
    "f_ring.02.L": ArmatureBoneInfo(
        parent_bone="f_ring.01.L",
    ),
    "f_ring.03.R": ArmatureBoneInfo(
        parent_bone="f_ring.02.R",
    ),
    "f_ring.03.L": ArmatureBoneInfo(
        parent_bone="f_ring.02.L",
    ),
    "palm.04.R": ArmatureBoneInfo(
        parent_bone="hand.R",
        connected=False,
        parent_position="head",
    ),
    "palm.04.L": ArmatureBoneInfo(
        parent_bone="hand.L",
        connected=False,
        parent_position="head",
    ),
    "f_pinky.01.R": ArmatureBoneInfo(
        parent_bone="palm.04.R",
    ),
    "f_pinky.01.L": ArmatureBoneInfo(
        parent_bone="palm.04.L",
    ),
    "f_pinky.02.R": ArmatureBoneInfo(
        parent_bone="f_pinky.01.R",
    ),
    "f_pinky.02.L": ArmatureBoneInfo(
        parent_bone="f_pinky.01.L",
    ),
    "f_pinky.03.R": ArmatureBoneInfo(
        parent_bone="f_pinky.02.R",
    ),
    "f_pinky.03.L": ArmatureBoneInfo(
        parent_bone="f_pinky.02.L",
    ),
    "thigh.R": ArmatureBoneInfo(
        parent_bone="pelvis.R",
    ),
    "thigh.L": ArmatureBoneInfo(
        parent_bone="pelvis.L",
    ),
    "shin.R": ArmatureBoneInfo(
        parent_bone="thigh.R",
    ),
    "shin.L": ArmatureBoneInfo(
        parent_bone="thigh.L",
    ),
    "foot.R": ArmatureBoneInfo(
        parent_bone="shin.R",
    ),
    "foot.L": ArmatureBoneInfo(
        parent_bone="shin.L",
    ),
    "heel.02.R": ArmatureBoneInfo(
        parent_bone="shin.R",
    ),
    "heel.02.L": ArmatureBoneInfo(
        parent_bone="shin.L",
    ),
}
