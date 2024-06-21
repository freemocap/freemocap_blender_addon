import math as m

from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import BoneRestPoseDefinition

freemocap_apose = {
    "pelvis": BoneRestPoseDefinition(
        rotation=(m.radians(-90), 0, 0),
    ),
    "pelvis.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-90), 0),
    ),
    "pelvis.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(90), 0),
    ),
    "spine": BoneRestPoseDefinition(
        rotation=(0, 0, 0),
    ),
    "spine.001": BoneRestPoseDefinition(
        rotation=(0, 0, 0),
    ),
    "neck": BoneRestPoseDefinition(
        rotation=(0, 0, 0),
    ),
    "face": BoneRestPoseDefinition(
        rotation=(m.radians(110), 0, 0),
    ),
    "shoulder.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-90), 0),
    ),
    "shoulder.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(90), 0),
    ),
    "upper_arm.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
        roll=m.radians(-135),
    ),
    "upper_arm.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
        roll=m.radians(135),
    ),
    "forearm.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(1)),
        roll=m.radians(-135),
    ),
    "forearm.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-1)),
        roll=m.radians(135),
    ),
    "hand.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "hand.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "thumb.carpal.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.carpal.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "thumb.01.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.01.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "thumb.02.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.02.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "thumb.03.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.03.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "palm.01.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(17)),
    ),
    "palm.01.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-17)),
    ),
    "f_index.01.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_index.01.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_index.02.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_index.02.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_index.03.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_index.03.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "palm.02.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(5.5)),
    ),
    "palm.02.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(-5.5)),
    ),
    "f_middle.01.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_middle.01.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_middle.02.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_middle.02.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_middle.03.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_middle.03.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "palm.03.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(-7.3)),
    ),
    "palm.03.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(7.3)),
    ),
    "f_ring.01.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_ring.01.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_ring.02.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_ring.02.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_ring.03.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_ring.03.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "palm.04.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), m.radians(-19)),
    ),
    "palm.04.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), m.radians(19)),
    ),
    "f_pinky.01.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_pinky.01.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_pinky.02.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_pinky.02.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_pinky.03.R": BoneRestPoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_pinky.03.L": BoneRestPoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "thigh.R": BoneRestPoseDefinition(
        rotation=(m.radians(1), m.radians(180), 0),
    ),
    "thigh.L": BoneRestPoseDefinition(
        rotation=(m.radians(1), m.radians(180), 0),
    ),
    "shin.R": BoneRestPoseDefinition(
        rotation=(m.radians(-1), m.radians(180), 0),
    ),
    "shin.L": BoneRestPoseDefinition(
        rotation=(m.radians(-1), m.radians(180), 0),
    ),
    "foot.R": BoneRestPoseDefinition(
        rotation=(m.radians(113), 0, 0),
    ),
    "foot.L": BoneRestPoseDefinition(
        rotation=(m.radians(113), 0, 0),
    ),
    "heel.02.R": BoneRestPoseDefinition(
        rotation=(m.radians(195), 0, 0),
    ),
    "heel.02.L": BoneRestPoseDefinition(
        rotation=(m.radians(195), 0, 0),
    ),
}
