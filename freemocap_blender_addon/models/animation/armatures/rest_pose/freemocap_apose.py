import math as m

from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import BonePoseDefinition

freemocap_apose = {
    "pelvis": BonePoseDefinition(
        rotation=(m.radians(-90), 0, 0),
    ),
    "pelvis.R": BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
    ),
    "pelvis.L": BonePoseDefinition(
        rotation=(0, m.radians(90), 0),
    ),
    "spine": BonePoseDefinition(
        rotation=(0, 0, 0),
    ),
    "spine.001": BonePoseDefinition(
        rotation=(0, 0, 0),
    ),
    "neck": BonePoseDefinition(
        rotation=(0, 0, 0),
    ),
    "face": BonePoseDefinition(
        rotation=(m.radians(110), 0, 0),
    ),
    "shoulder.R": BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
    ),
    "shoulder.L": BonePoseDefinition(
        rotation=(0, m.radians(90), 0),
    ),
    "upper_arm.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
        roll=m.radians(-135),
    ),
    "upper_arm.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
        roll=m.radians(135),
    ),
    "forearm.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(1)),
        roll=m.radians(-135),
    ),
    "forearm.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-1)),
        roll=m.radians(135),
    ),
    "hand.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "hand.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "thumb.carpal.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.carpal.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "thumb.01.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.01.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "thumb.02.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.02.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "thumb.03.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(45)),
    ),
    "thumb.03.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-45)),
    ),
    "palm.01.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(17)),
    ),
    "palm.01.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-17)),
    ),
    "f_index.01.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_index.01.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_index.02.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_index.02.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_index.03.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_index.03.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "palm.02.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(5.5)),
    ),
    "palm.02.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(-5.5)),
    ),
    "f_middle.01.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_middle.01.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_middle.02.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_middle.02.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_middle.03.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_middle.03.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "palm.03.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(-7.3)),
    ),
    "palm.03.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(7.3)),
    ),
    "f_ring.01.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_ring.01.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_ring.02.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_ring.02.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_ring.03.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_ring.03.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "palm.04.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), m.radians(-19)),
    ),
    "palm.04.L": BonePoseDefinition(
        rotation=(0, m.radians(135), m.radians(19)),
    ),
    "f_pinky.01.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_pinky.01.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_pinky.02.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_pinky.02.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "f_pinky.03.R": BonePoseDefinition(
        rotation=(0, m.radians(-135), 0),
    ),
    "f_pinky.03.L": BonePoseDefinition(
        rotation=(0, m.radians(135), 0),
    ),
    "thigh.R": BonePoseDefinition(
        rotation=(m.radians(1), m.radians(180), 0),
    ),
    "thigh.L": BonePoseDefinition(
        rotation=(m.radians(1), m.radians(180), 0),
    ),
    "shin.R": BonePoseDefinition(
        rotation=(m.radians(-1), m.radians(180), 0),
    ),
    "shin.L": BonePoseDefinition(
        rotation=(m.radians(-1), m.radians(180), 0),
    ),
    "foot.R": BonePoseDefinition(
        rotation=(m.radians(113), 0, 0),
    ),
    "foot.L": BonePoseDefinition(
        rotation=(m.radians(113), 0, 0),
    ),
    "heel.02.R": BonePoseDefinition(
        rotation=(m.radians(195), 0, 0),
    ),
    "heel.02.L": BonePoseDefinition(
        rotation=(m.radians(195), 0, 0),
    ),
}
