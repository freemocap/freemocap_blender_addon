import math as m

from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement

freemocap_tpose = {
    "pelvis": PoseElement(
        rotation=(m.radians(-90), 0, 0),
    ),
    "pelvis.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "pelvis.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "spine": PoseElement(
        rotation=(0, 0, 0),
    ),
    "spine.001": PoseElement(
        rotation=(0, 0, 0),
    ),
    "neck": PoseElement(
        rotation=(0, 0, 0),
    ),
    "face": PoseElement(
        rotation=(m.radians(110), 0, 0),
    ),
    "shoulder.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "shoulder.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "upper_arm.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
        roll=m.radians(-90),
    ),
    "upper_arm.L": PoseElement(
        rotation=(0, m.radians(90), 0),
        roll=m.radians(90),
    ),
    "forearm.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(1)),
        roll=m.radians(-90),
    ),
    "forearm.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-1)),
        roll=m.radians(90),
    ),
    "hand.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
        roll=m.radians(-90),
    ),
    "hand.L": PoseElement(
        rotation=(0, m.radians(90), 0),
        roll=m.radians(90),
    ),
    "thumb.carpal.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(45)),
    ),
    "thumb.carpal.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-45)),
    ),
    "thumb.01.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(45)),
    ),
    "thumb.01.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-45)),
    ),
    "thumb.02.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(45)),
    ),
    "thumb.02.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-45)),
    ),
    "thumb.03.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(45)),
    ),
    "thumb.03.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-45)),
    ),
    "palm.01.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(17)),
    ),
    "palm.01.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-17)),
    ),
    "f_index.01.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_index.01.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_index.02.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_index.02.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_index.03.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_index.03.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "palm.02.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(5.5)),
    ),
    "palm.02.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(-5.5)),
    ),
    "f_middle.01.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_middle.01.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_middle.02.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_middle.02.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_middle.03.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_middle.03.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "palm.03.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(-7.3)),
    ),
    "palm.03.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(7.3)),
    ),
    "f_ring.01.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_ring.01.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_ring.02.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_ring.02.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_ring.03.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_ring.03.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "palm.04.R": PoseElement(
        rotation=(0, m.radians(-90), m.radians(-19)),
    ),
    "palm.04.L": PoseElement(
        rotation=(0, m.radians(90), m.radians(19)),
    ),
    "f_pinky.01.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_pinky.01.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_pinky.02.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_pinky.02.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "f_pinky.03.R": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "f_pinky.03.L": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "thigh.R": PoseElement(
        rotation=(m.radians(1), m.radians(180), 0),
    ),
    "thigh.L": PoseElement(
        rotation=(m.radians(1), m.radians(180), 0),
    ),
    "shin.R": PoseElement(
        rotation=(m.radians(-1), m.radians(180), 0),
    ),
    "shin.L": PoseElement(
        rotation=(m.radians(-1), m.radians(180), 0),
    ),
    "foot.R": PoseElement(
        rotation=(m.radians(113), 0, 0),
    ),
    "foot.L": PoseElement(
        rotation=(m.radians(113), 0, 0),
    ),
    "heel.02.R": PoseElement(
        rotation=(m.radians(195), 0, 0),
    ),
    "heel.02.L": PoseElement(
        rotation=(m.radians(195), 0, 0),
    ),
}
