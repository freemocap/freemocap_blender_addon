# from freemocap_blender_addon.models.animation.armatures.armature_bone_info import (
#     ArmatureBoneDefinition,
# )
#
#
# armature_freemocap = {
#     "pelvis": ArmatureBoneDefinition(
#         parent_bone_name="root",
#         is_connected=False,
#         parent_position="head",
#         length=0.05,
#     ),
#     "pelvis.R": ArmatureBoneDefinition(
#         parent_bone_name="pelvis",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "pelvis.L": ArmatureBoneDefinition(
#         parent_bone_name="pelvis",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "spine": ArmatureBoneDefinition(
#         parent_bone_name="pelvis",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "spine.001": ArmatureBoneDefinition(
#         parent_bone_name="spine",
#     ),
#     "neck": ArmatureBoneDefinition(
#         parent_bone_name="spine.001",
#     ),
#     "face": ArmatureBoneDefinition(
#         parent_bone_name="neck",
#         length=0.1,
#     ),
#     "shoulder.R": ArmatureBoneDefinition(
#         parent_bone_name="spine.001",
#     ),
#     "shoulder.L": ArmatureBoneDefinition(
#         parent_bone_name="spine.001",
#     ),
#     "upper_arm.R": ArmatureBoneDefinition(
#         parent_bone_name="shoulder.R",
#     ),
#     "upper_arm.L": ArmatureBoneDefinition(
#         parent_bone_name="shoulder.L",
#     ),
#     "forearm.R": ArmatureBoneDefinition(
#         parent_bone_name="upper_arm.R",
#     ),
#     "forearm.L": ArmatureBoneDefinition(
#         parent_bone_name="upper_arm.L",
#     ),
#     "hand.R": ArmatureBoneDefinition(
#         parent_bone_name="forearm.R",
#     ),
#     "hand.L": ArmatureBoneDefinition(
#         parent_bone_name="forearm.L",
#     ),
#     "thumb.carpal.R": ArmatureBoneDefinition(
#         parent_bone_name="hand.R",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "thumb.carpal.L": ArmatureBoneDefinition(
#         parent_bone_name="hand.L",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "thumb.01.R": ArmatureBoneDefinition(
#         parent_bone_name="thumb.carpal.R",
#     ),
#     "thumb.01.L": ArmatureBoneDefinition(
#         parent_bone_name="thumb.carpal.L",
#     ),
#     "thumb.02.R": ArmatureBoneDefinition(
#         parent_bone_name="thumb.01.R",
#     ),
#     "thumb.02.L": ArmatureBoneDefinition(
#         parent_bone_name="thumb.01.L",
#     ),
#     "thumb.03.R": ArmatureBoneDefinition(
#         parent_bone_name="thumb.02.R",
#     ),
#     "thumb.03.L": ArmatureBoneDefinition(
#         parent_bone_name="thumb.02.L",
#     ),
#     "palm.01.R": ArmatureBoneDefinition(
#         parent_bone_name="hand.R",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "palm.01.L": ArmatureBoneDefinition(
#         parent_bone_name="hand.L",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "f_index.01.R": ArmatureBoneDefinition(
#         parent_bone_name="palm.01.R",
#     ),
#     "f_index.01.L": ArmatureBoneDefinition(
#         parent_bone_name="palm.01.L",
#     ),
#     "f_index.02.R": ArmatureBoneDefinition(
#         parent_bone_name="f_index.01.R",
#     ),
#     "f_index.02.L": ArmatureBoneDefinition(
#         parent_bone_name="f_index.01.L",
#     ),
#     "f_index.03.R": ArmatureBoneDefinition(
#         parent_bone_name="f_index.02.R",
#     ),
#     "f_index.03.L": ArmatureBoneDefinition(
#         parent_bone_name="f_index.02.L",
#     ),
#     "palm.02.R": ArmatureBoneDefinition(
#         parent_bone_name="hand.R",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "palm.02.L": ArmatureBoneDefinition(
#         parent_bone_name="hand.L",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "f_middle.01.R": ArmatureBoneDefinition(
#         parent_bone_name="palm.02.R",
#     ),
#     "f_middle.01.L": ArmatureBoneDefinition(
#         parent_bone_name="palm.02.L",
#     ),
#     "f_middle.02.R": ArmatureBoneDefinition(
#         parent_bone_name="f_middle.01.R",
#     ),
#     "f_middle.02.L": ArmatureBoneDefinition(
#         parent_bone_name="f_middle.01.L",
#     ),
#     "f_middle.03.R": ArmatureBoneDefinition(
#         parent_bone_name="f_middle.02.R",
#     ),
#     "f_middle.03.L": ArmatureBoneDefinition(
#         parent_bone_name="f_middle.02.L",
#     ),
#     "palm.03.R": ArmatureBoneDefinition(
#         parent_bone_name="hand.R",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "palm.03.L": ArmatureBoneDefinition(
#         parent_bone_name="hand.L",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "f_ring.01.R": ArmatureBoneDefinition(
#         parent_bone_name="palm.03.R",
#     ),
#     "f_ring.01.L": ArmatureBoneDefinition(
#         parent_bone_name="palm.03.L",
#     ),
#     "f_ring.02.R": ArmatureBoneDefinition(
#         parent_bone_name="f_ring.01.R",
#     ),
#     "f_ring.02.L": ArmatureBoneDefinition(
#         parent_bone_name="f_ring.01.L",
#     ),
#     "f_ring.03.R": ArmatureBoneDefinition(
#         parent_bone_name="f_ring.02.R",
#     ),
#     "f_ring.03.L": ArmatureBoneDefinition(
#         parent_bone_name="f_ring.02.L",
#     ),
#     "palm.04.R": ArmatureBoneDefinition(
#         parent_bone_name="hand.R",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "palm.04.L": ArmatureBoneDefinition(
#         parent_bone_name="hand.L",
#         is_connected=False,
#         parent_position="head",
#     ),
#     "f_pinky.01.R": ArmatureBoneDefinition(
#         parent_bone_name="palm.04.R",
#     ),
#     "f_pinky.01.L": ArmatureBoneDefinition(
#         parent_bone_name="palm.04.L",
#     ),
#     "f_pinky.02.R": ArmatureBoneDefinition(
#         parent_bone_name="f_pinky.01.R",
#     ),
#     "f_pinky.02.L": ArmatureBoneDefinition(
#         parent_bone_name="f_pinky.01.L",
#     ),
#     "f_pinky.03.R": ArmatureBoneDefinition(
#         parent_bone_name="f_pinky.02.R",
#     ),
#     "f_pinky.03.L": ArmatureBoneDefinition(
#         parent_bone_name="f_pinky.02.L",
#     ),
#     "thigh.R": ArmatureBoneDefinition(
#         parent_bone_name="pelvis.R",
#     ),
#     "thigh.L": ArmatureBoneDefinition(
#         parent_bone_name="pelvis.L",
#     ),
#     "shin.R": ArmatureBoneDefinition(
#         parent_bone_name="thigh.R",
#     ),
#     "shin.L": ArmatureBoneDefinition(
#         parent_bone_name="thigh.L",
#     ),
#     "foot.R": ArmatureBoneDefinition(
#         parent_bone_name="shin.R",
#     ),
#     "foot.L": ArmatureBoneDefinition(
#         parent_bone_name="shin.L",
#     ),
#     "heel.02.R": ArmatureBoneDefinition(
#         parent_bone_name="shin.R",
#     ),
#     "heel.02.L": ArmatureBoneDefinition(
#         parent_bone_name="shin.L",
#     ),
# }
