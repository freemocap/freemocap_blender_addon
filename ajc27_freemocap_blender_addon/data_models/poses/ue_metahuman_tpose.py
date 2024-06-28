import math as m

from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement

ue_metahuman_tpose = {
    "pelvis": PoseElement(
        rotation=(
            m.radians(-90),
            0,
            0,
        ),
    ),
    "pelvis_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
    ),
    "pelvis_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
    ),
    "spine_01": PoseElement(
        rotation=(
            m.radians(6),
            0,
            0,
        ),
    ),
    "spine_04": PoseElement(
        rotation=(
            m.radians(-9.86320126530132),
            0,
            0,
        ),
    ),
    "neck_01": PoseElement(
        rotation=(
            m.radians(11.491515802111422),
            0,
            0,
        ),
    ),
    "face": PoseElement(
        rotation=(
            m.radians(110),
            0,
            0,
        ),
    ),
    "clavicle_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
    ),
    "clavicle_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
    ),
    "upperarm_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(-90),
    ),
    "upperarm_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(90),
    ),
    "lowerarm_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(1),
        ),
        roll=m.radians(-90),
    ),
    "lowerarm_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-1),
        ),
        roll=m.radians(90),
    ),
    "hand_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(-90),
    ),
    "hand_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(90),
    ),
    "thumb_metacarpal_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(45),
        ),
        roll=m.radians(-69),
    ),
    "thumb_01_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(45),
        ),
        roll=m.radians(-69),
    ),
    "thumb_02_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(45),
        ),
        roll=m.radians(-69),
    ),
    "thumb_03_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(45),
        ),
        roll=m.radians(-69),
    ),
    "thumb_metacarpal_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-45),
        ),
        roll=m.radians(69),
    ),
    "thumb_01_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-45),
        ),
        roll=m.radians(69),
    ),
    "thumb_02_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-45),
        ),
        roll=m.radians(69),
    ),
    "thumb_03_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-45),
        ),
        roll=m.radians(69),
    ),
    "index_metacarpal_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(17),
        ),
        roll=m.radians(0),
    ),
    "index_01_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "index_02_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "index_03_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "index_metacarpal_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-17),
        ),
        roll=m.radians(0),
    ),
    "index_01_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "index_02_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "index_03_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "middle_metacarpal_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(5.5),
        ),
        roll=m.radians(0),
    ),
    "middle_01_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "middle_02_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "middle_03_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "middle_metacarpal_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(-5.5),
        ),
        roll=m.radians(0),
    ),
    "middle_01_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "middle_02_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "middle_03_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "ring_metacarpal_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(-7.3),
        ),
        roll=m.radians(0),
    ),
    "ring_01_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "ring_02_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "ring_03_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "ring_metacarpal_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(7.3),
        ),
        roll=m.radians(0),
    ),
    "ring_01_l": PoseElement(rotation=(0, m.radians(90), 0), roll=m.radians(0)),
    "ring_02_l": PoseElement(rotation=(0, m.radians(90), 0), roll=m.radians(0)),
    "ring_03_l": PoseElement(rotation=(0, m.radians(90), 0), roll=m.radians(0)),
    "pinky_metacarpal_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            m.radians(-19),
        ),
        roll=m.radians(0),
    ),
    "pinky_01_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "pinky_02_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "pinky_03_r": PoseElement(
        rotation=(
            0,
            m.radians(-90),
            0,
        ),
        roll=m.radians(0),
    ),
    "pinky_metacarpal_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            m.radians(19),
        ),
        roll=m.radians(0),
    ),
    "pinky_01_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "pinky_02_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "pinky_03_l": PoseElement(
        rotation=(
            0,
            m.radians(90),
            0,
        ),
        roll=m.radians(0),
    ),
    "thigh_r": PoseElement(
        rotation=(
            m.radians(1),
            m.radians(-176.63197042733134),
            m.radians(4.106872792731369),
        ),
        roll=m.radians(101),
    ),
    "thigh_l": PoseElement(
        rotation=(
            m.radians(1),
            m.radians(176.63197042733134),
            m.radians(-4.106635016770888),
        ),
        roll=m.radians(-101),
    ),
    "calf_r": PoseElement(
        rotation=(
            m.radians(-175.12260790378525),
            m.radians(-2.6481038282450826),
            m.radians(56.97761905625937),
        ),
        roll=m.radians(101),
    ),
    "calf_l": PoseElement(
        rotation=(
            m.radians(-175.12259424340692),
            m.radians(2.648141394285518),
            m.radians(-56.97820303743341),
        ),
        roll=m.radians(-101),
    ),
    "foot_r": PoseElement(
        rotation=(
            m.radians(106.8930615673465),
            m.radians(-8.188085418524645),
            m.radians(-11.028648396211644),
        ),
        roll=m.radians(90),
    ),
    "foot_l": PoseElement(
        rotation=(
            m.radians(107.86645231653254),
            m.radians(8.93590490150277),
            m.radians(12.247207078107985),
        ),
        roll=m.radians(-90),
    ),
    "heel_r": PoseElement(
        rotation=(m.radians(195), 0, 0),
    ),
    "heel_l": PoseElement(
        rotation=(m.radians(195), 0, 0),
    ),
}
