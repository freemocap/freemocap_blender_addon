import math as m

from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement

ue_metahuman_default = {
    "pelvis": PoseElement(
        rotation=(m.radians(-90), 0, 0),
    ),
    "pelvis_r": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "pelvis_l": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "spine_01": PoseElement(
        rotation=(m.radians(6), 0, 0),
    ),
    "spine_04": PoseElement(
        rotation=(m.radians(-9.86320126530132), 0, 0),
    ),
    "neck_01": PoseElement(
        rotation=(m.radians(11.491515802111422), 0, 0),
    ),
    "face": PoseElement(
        rotation=(m.radians(110), 0, 0),
    ),
    "clavicle_r": PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    "clavicle_l": PoseElement(
        rotation=(0, m.radians(90), 0),
    ),
    "upperarm_r": PoseElement(
        rotation=(
            m.radians(-2.6811034603331763),
            m.radians(-144.74571040036872),
            m.radians(8.424363006256543),
        ),
        roll=m.radians(130),
    ),
    "upperarm_l": PoseElement(
        rotation=(
            m.radians(-2.6811482834496045),
            m.radians(144.74547817393693),
            m.radians(-8.42444582230023),
        ),
        roll=m.radians(-130),
    ),
    "lowerarm_r": PoseElement(
        rotation=(
            m.radians(131.9406083482122),
            m.radians(-28.645770690351164),
            m.radians(-59.596439942541906),
        ),
        roll=m.radians(136),
    ),
    "lowerarm_l": PoseElement(
        rotation=(
            m.radians(131.94101815956242),
            m.radians(28.64569726581759),
            m.radians(59.596774621811235),
        ),
        roll=m.radians(-136),
    ),
    "hand_r": PoseElement(
        rotation=(
            m.radians(136.60972566483292),
            m.radians(-19.358236551318736),
            m.radians(-46.40956446672754),
        ),
        roll=m.radians(-178),
    ),
    "hand_l": PoseElement(
        rotation=(
            m.radians(136.47491139099523),
            m.radians(18.1806521742533),
            m.radians(43.68087998764535),
        ),
        roll=m.radians(178),
    ),
    "thumb_metacarpal_r": PoseElement(
        rotation=(
            m.radians(108.46138911399733),
            m.radians(29.91067562086063),
            m.radians(40.68765203672481),
        ),
        roll=m.radians(118.0),
    ),
    "thumb_01_r": PoseElement(
        rotation=(
            m.radians(117.97956508092275),
            m.radians(12.793343881500329),
            m.radians(21.12921239554925),
        ),
        roll=m.radians(22.0),
    ),
    "thumb_02_r": PoseElement(
        rotation=(
            m.radians(139.66359886539402),
            m.radians(4.185290621479108),
            m.radians(11.362482429632479),
        ),
        roll=m.radians(58.0),
    ),
    "thumb_03_r": PoseElement(
        rotation=(
            m.radians(139.66359886539402),
            m.radians(4.185290621479108),
            m.radians(11.362482429632479),
        ),
        roll=m.radians(-86.0),
    ),
    "thumb_metacarpal_l": PoseElement(
        rotation=(
            m.radians(129.87864253967706),
            m.radians(-29.566061841382222),
            m.radians(-58.87750789088471),
        ),
        roll=m.radians(-118.0),
    ),
    "thumb_01_l": PoseElement(
        rotation=(
            m.radians(122.88600415044473),
            m.radians(-10.369630763953793),
            m.radians(-18.93130874705792),
        ),
        roll=m.radians(-8.3),
    ),
    "thumb_02_l": PoseElement(
        rotation=(
            m.radians(152.60762696526857),
            m.radians(0.13829642967458847),
            m.radians(0.5674746878854321),
        ),
        roll=m.radians(-49.0),
    ),
    "thumb_03_l": PoseElement(
        rotation=(
            m.radians(152.60762696526857),
            m.radians(0.13829642967458847),
            m.radians(0.5674746878854321),
        ),
        roll=m.radians(88.0),
    ),
    "index_metacarpal_r": PoseElement(
        rotation=(
            m.radians(123.54290442405987),
            m.radians(-18.78471410444923),
            m.radians(-34.25055391382464),
        ),
        roll=m.radians(-168.0),
    ),
    "index_01_r": PoseElement(
        rotation=(
            m.radians(146.31965919270647),
            m.radians(-5.665469027362211),
            m.radians(-18.568524956839983),
        ),
        roll=m.radians(-71.0),
    ),
    "index_02_r": PoseElement(
        rotation=(
            m.radians(161.1726022221945),
            m.radians(1.1799849751152838),
            m.radians(7.108271784333358),
        ),
        roll=m.radians(131.0),
    ),
    "index_03_r": PoseElement(
        rotation=(
            m.radians(161.1726022221945),
            m.radians(1.1799725953974132),
            m.radians(7.108197079139311),
        ),
        roll=m.radians(-106.0),
    ),
    "index_metacarpal_l": PoseElement(
        rotation=(
            m.radians(122.2014962522044),
            m.radians(16.459000541114037),
            m.radians(29.363099355100708),
        ),
        roll=m.radians(168.0),
    ),
    "index_01_l": PoseElement(
        rotation=(
            m.radians(154.4863387983723),
            m.radians(-2.002480837279862),
            m.radians(-8.828185134328853),
        ),
        roll=m.radians(-167.0),
    ),
    "index_02_l": PoseElement(
        rotation=(
            m.radians(167.53544252843832),
            m.radians(-6.072667830205446),
            m.radians(-51.81414972298606),
        ),
        roll=m.radians(-138.0),
    ),
    "index_03_l": PoseElement(
        rotation=(
            m.radians(167.53531958503328),
            m.radians(-6.072608492937031),
            m.radians(-51.81328228896147),
        ),
        roll=m.radians(83.0),
    ),
    "middle_metacarpal_r": PoseElement(
        rotation=(
            m.radians(135.85862342218496),
            m.radians(-27.633989155387788),
            m.radians(-62.47886173455733),
        ),
        roll=m.radians(-163.0),
    ),
    "middle_01_r": PoseElement(
        rotation=(
            m.radians(150.7975995144585),
            m.radians(-8.823725874574482),
            m.radians(-32.99580376706369),
        ),
        roll=m.radians(172.0),
    ),
    "middle_02_r": PoseElement(
        rotation=(
            m.radians(164.517796651235),
            m.radians(12.618237467975066),
            m.radians(78.24571139574978),
        ),
        roll=m.radians(-103.0),
    ),
    "middle_03_r": PoseElement(
        rotation=(
            m.radians(164.517796651235),
            m.radians(12.618237467975066),
            m.radians(78.24571139574978),
        ),
        roll=m.radians(-93.0),
    ),
    "middle_metacarpal_l": PoseElement(
        rotation=(
            m.radians(135.8578857617546),
            m.radians(27.63338468364624),
            m.radians(62.476764866482135),
        ),
        roll=m.radians(163.0),
    ),
    "middle_01_l": PoseElement(
        rotation=(
            m.radians(153.59596899854776),
            m.radians(2.9706012417475782),
            m.radians(12.614850547920385),
        ),
        roll=m.radians(172.0),
    ),
    "middle_02_l": PoseElement(
        rotation=(
            m.radians(-12.509869686603643),
            m.radians(-161.1841315815135),
            m.radians(66.96937643457139),
        ),
        roll=m.radians(103.0),
    ),
    "middle_03_l": PoseElement(
        rotation=(
            m.radians(-12.509869686603643),
            m.radians(-161.1841315815135),
            m.radians(66.96937643457139),
        ),
        roll=m.radians(93.0),
    ),
    "ring_metacarpal_r": PoseElement(
        rotation=(
            m.radians(-35.38173227812171),
            m.radians(-144.13648484716026),
            m.radians(89.17283244504377),
        ),
        roll=m.radians(-158.0),
    ),
    "ring_01_r": PoseElement(
        rotation=(
            m.radians(157.3626134201347),
            m.radians(-10.553912682855323),
            m.radians(-49.541062767205815),
        ),
        roll=m.radians(-175.0),
    ),
    "ring_02_r": PoseElement(
        rotation=(
            m.radians(166.01302068319916),
            m.radians(5.336361484847024),
            m.radians(41.603730668585264),
        ),
        roll=m.radians(151.0),
    ),
    "ring_03_r": PoseElement(
        rotation=(
            m.radians(166.01302068319916),
            m.radians(5.336361484847024),
            m.radians(41.603730668585264),
        ),
        roll=m.radians(151.0),
    ),
    "ring_metacarpal_l": PoseElement(
        rotation=(
            m.radians(-35.38086484409712),
            m.radians(144.13655314905196),
            m.radians(-89.17146640720976),
        ),
        roll=m.radians(158.0),
    ),
    "ring_01_l": PoseElement(
        rotation=(
            m.radians(158.7280911786253),
            m.radians(-1.3540651527177525),
            m.radians(-7.201199923085966),
        ),
        roll=m.radians(175.0),
    ),
    "ring_02_l": PoseElement(
        rotation=(
            m.radians(163.8374688287667),
            m.radians(-9.297557441639421),
            m.radians(-59.59876903704888),
        ),
        roll=m.radians(-151.0),
    ),
    "ring_03_l": PoseElement(
        rotation=(
            m.radians(163.8374688287667),
            m.radians(-9.297557441639421),
            m.radians(-59.59876903704888),
        ),
        roll=m.radians(-151.0),
    ),
    "pinky_metacarpal_r": PoseElement(
        rotation=(
            m.radians(-22.97185570719341),
            m.radians(-145.80376134431705),
            m.radians(66.89572650475114),
        ),
        roll=m.radians(-157.0),
    ),
    "pinky_01_r": PoseElement(
        rotation=(
            m.radians(163.10432998363586),
            m.radians(-13.879361888778927),
            m.radians(-78.67092482252893),
        ),
        roll=m.radians(-170.0),
    ),
    "pinky_02_r": PoseElement(
        rotation=(
            m.radians(168.97607968855576),
            m.radians(4.6775274139231175),
            m.radians(45.879312975797355),
        ),
        roll=m.radians(-95.0),
    ),
    "pinky_03_r": PoseElement(
        rotation=(
            m.radians(162.22981988306412),
            m.radians(2.758289507152786),
            m.radians(17.509948088325558),
        ),
        roll=m.radians(-80.0),
    ),
    "pinky_metacarpal_l": PoseElement(
        rotation=(
            m.radians(-22.97141174489736),
            m.radians(145.80314662729177),
            m.radians(-66.8936842781893),
        ),
        roll=m.radians(157.0),
    ),
    "pinky_01_l": PoseElement(
        rotation=(
            m.radians(164.59784646830755),
            m.radians(6.764079769036197),
            m.radians(47.212989373512386),
        ),
        roll=m.radians(170.0),
    ),
    "pinky_02_l": PoseElement(
        rotation=(
            m.radians(-9.264448953411431),
            m.radians(-169.27331586085637),
            m.radians(81.59100144743863),
        ),
        roll=m.radians(95.0),
    ),
    "pinky_03_l": PoseElement(
        rotation=(
            m.radians(163.6619739482324),
            m.radians(-9.964792645242444),
            m.radians(-62.541241852247055),
        ),
        roll=m.radians(97.0),
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
