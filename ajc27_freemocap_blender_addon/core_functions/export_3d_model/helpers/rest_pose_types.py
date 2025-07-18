import math as m

rest_pose_type_rotations = {
    'metahuman': {
        'pelvis': {
            'rotation' : (
                m.radians(-90),
                0,
                0
            ),
            'roll': 0,
        },
        'pelvis.R': {
            'rotation' : (
                0,
                m.radians(-90),
                0
            ),
            'roll': 0,
        },
        'pelvis.L': {
            'rotation' : (
                0,
                m.radians(90),
                0
            ),
            'roll': 0,
        },
        'spine': {
            'rotation' : (
                m.radians(6),
                0,
                0
            ),
            'roll': 0,
        },
        'spine.001': {
            'rotation' : (
                m.radians(-9.86320126530132),
                0,
                0
            ),
            'roll': 0,
        },
        'neck': {
            'rotation' : (
                m.radians(11.491515802111422),
                0,
                0
            ),
            'roll': 0,
        },
        'face': {
            'rotation' : (
                m.radians(110),
                0,
                0
            ),
            'roll': 0,
        },
        'shoulder.R': {
            'rotation' : (
                0,
                m.radians(-90),
                0
            ),
            'roll': 0,
        },
        'shoulder.L': {
            'rotation' : (
                0,
                m.radians(90),
                0
            ),
            'roll': 0,
        },
        'upper_arm.R': {
            'rotation' : (
                m.radians(-2.6811034603331763),
                m.radians(-144.74571040036872),
                m.radians(8.424363006256543),
            ),
            'roll': m.radians(130),
        },
        'upper_arm.L': {
            'rotation' : (
                m.radians(-2.6811482834496045),
                m.radians(144.74547817393693),
                m.radians(-8.42444582230023),
            ),
            'roll': m.radians(-130.6438),
            # 'roll': m.radians(49.3562),
        },
        'forearm.R': {
            'rotation' : (
                m.radians(131.9406083482122),
                m.radians(-28.645770690351164),
                m.radians(-59.596439942541906),
            ),
            'roll': m.radians(136),
        },
        'forearm.L': {
            'rotation' : (
                m.radians(131.94101815956242),
                m.radians(28.64569726581759),
                m.radians(59.596774621811235),
            ),
            # 'roll': m.radians(-136),
            'roll': m.radians(-134.0328),
            # 'roll': m.radians(-38.6328),
        },
        'hand.R': {
            'rotation' : (
                m.radians(136.60972566483292),
                m.radians(-19.358236551318736),
                m.radians(-46.40956446672754),
            ),
            'roll': m.radians(-178),
        },
        'hand.L': {
            'rotation' : (
                # m.radians(136.47491139099523),
                # m.radians(18.1806521742533),
                # m.radians(43.68087998764535),
                m.radians(134.37488776840476),
                m.radians(30.27156232603659),
                m.radians(65.48831821494582),
            ),
            # 'roll': m.radians(178),
            'roll': m.radians(-224.0328),
            # 'roll': m.radians(135.9672),
        },
        'thumb.carpal.R': {
            'rotation' : (
                m.radians(108.46138911399733),
                m.radians(29.91067562086063),
                m.radians(40.68765203672481),
            ),
            'roll' : m.radians(118.0)
        },
        'thumb.01.R': {
            'rotation' : (
                m.radians(117.97956508092275),
                m.radians(12.793343881500329),
                m.radians(21.12921239554925),
            ),
            'roll' : m.radians(22.0)
        },
        'thumb.02.R': {
            'rotation' : (
                m.radians(139.66359886539402),
                m.radians(4.185290621479108),
                m.radians(11.362482429632479),
            ),
            'roll' : m.radians(58.0)
        },
        'thumb.03.R': {
            'rotation' : (
                m.radians(139.66359886539402),
                m.radians(4.185290621479108),
                m.radians(11.362482429632479),
            ),
            'roll' : m.radians(-86.0)
        },
        'thumb.carpal.L': {
            'rotation' : (
                # m.radians(129.87864253967706),
                # m.radians(-29.566061841382222),
                # m.radians(-58.87750789088471),
                m.radians(100.00107242),
                m.radians(-22.19237119),
                m.radians(-26.31167102),
            ),
            'roll' : m.radians(-118.0)
        },
        'thumb.01.L': {
            'rotation' : (
                # m.radians(122.88600415044473),
                # m.radians(-10.369630763953793),
                # m.radians(-18.93130874705792),
                m.radians(111.221086067),
                m.radians(-2.7829123391),
                m.radians(-4.0650395916),
            ),
            # 'roll' : m.radians(-8.3)
            'roll' : m.radians(116.861)
        },
        'thumb.02.L': {
            'rotation' : (
                # m.radians(152.60762696526857),
                # m.radians(0.13829642967458847),
                # m.radians(0.5674746878854321),
                m.radians(130.7663349053),
                m.radians(1.4840594474),
                m.radians(3.2382712327),
            ),
            'roll' : m.radians(98.3163)
        },
        'thumb.03.L': {
            'rotation' : (
                # m.radians(152.60762696526857),
                # m.radians(0.13829642967458847),
                # m.radians(0.5674746878854321),
                m.radians(140.5535588539),
                m.radians(3.584009432),
                m.radians(9.9749704809),
            ),
            'roll' : m.radians(94.2938)
        },
        'palm.01.R': {
            'rotation' : (
                m.radians(123.54290442405987),
                m.radians(-18.78471410444923),
                m.radians(-34.25055391382464),
            ),
            'roll' : m.radians(-168.0)
        },
        'f_index.01.R': {
            'rotation' : (
                m.radians(146.31965919270647),
                m.radians(-5.665469027362211),
                m.radians(-18.568524956839983),
            ),
            'roll' : m.radians(-71.0)
        },
        'f_index.02.R': {
            'rotation' : (
                m.radians(161.1726022221945),
                m.radians(1.1799849751152838),
                m.radians(7.108271784333358),
            ),
            'roll' : m.radians(131.0)
        },
        'f_index.03.R': {
            'rotation' : (
                m.radians(161.1726022221945),
                m.radians(1.1799725953974132),
                m.radians(7.108197079139311),
            ),
            'roll' : m.radians(-106.0)
        },
        'palm.01.L': {
            'rotation' : (
                # m.radians(122.2014962522044),
                # m.radians(16.459000541114037),
                # m.radians(29.363099355100708),
                m.radians(128.135305055923),
                m.radians(27.77213826908776),
                m.radians(53.89689296697639),
            ),
            'roll' : m.radians(-37.0419),
            'position_offset' : {
                'wrist_newbonehead_to_wrist_mcp_ratio' : 0.436234137, # Multiply this by bone the length to get the bone distance from the hand bone head
                'newbonehead_mcp_to_wrist_mcp_ratio': 0.596401283365858,
                'rotation' : ( # Rotation of the vector (0, 0, (hand_head to bone head)) to get the new bone head position
                    m.radians(103.22881534179642),
                    m.radians(10.22773102262584),
                    m.radians(12.890593822450262),
                )
            }
        },
        'f_index.01.L': {
            'rotation' : (
                # m.radians(154.4863387983723),
                # m.radians(-2.002480837279862),
                # m.radians(-8.828185134328853),
                m.radians(139.3933282799366),
                m.radians(10.794142388795718),
                m.radians(28.64949143590153),
            ),
            'roll' : m.radians(7.11665)
        },
        'f_index.02.L': {
            'rotation' : (
                # m.radians(167.53544252843832),
                # m.radians(-6.072667830205446),
                # m.radians(-51.81414972298606),
                m.radians(145.4210112036079),
                m.radians(0.39639077553363045),
                m.radians(1.273439251877395),
            ),
            'roll' : m.radians(28.9898)
        },
        'f_index.03.L': {
            'rotation' : (
                # m.radians(167.53531958503328),
                # m.radians(-6.072608492937031),
                # m.radians(-51.81328228896147),
                m.radians(147.40724387462592),
                m.radians(-3.076360317742879),
                m.radians(-10.49587741925137),
            ),
            'roll' : m.radians(35.4056)
        },
        'palm.02.R': {
            'rotation' : (
                m.radians(135.85862342218496),
                m.radians(-27.633989155387788),
                m.radians(-62.47886173455733),
            ),
            'roll' : m.radians(-163.0)
        },
        'f_middle.01.R': {
            'rotation' : (
                m.radians(150.7975995144585),
                m.radians(-8.823725874574482),
                m.radians(-32.99580376706369),
            ),
            'roll' : m.radians(172.0)
        },
        'f_middle.02.R': {
            'rotation' : (
                m.radians(164.517796651235),
                m.radians(12.618237467975066),
                m.radians(78.24571139574978),
            ),
            'roll' : m.radians(-103.0)
        },
        'f_middle.03.R': {
            'rotation' : (
                m.radians(164.517796651235),
                m.radians(12.618237467975066),
                m.radians(78.24571139574978),
            ),
            'roll' : m.radians(-93.0)
        },
        'palm.02.L': {
            'rotation' : (
                # m.radians(135.8578857617546),
                # m.radians(27.63338468364624),
                # m.radians(62.476764866482135),
                m.radians(133.10490971488926),
                m.radians(35.25740917484914),
                m.radians(72.45711241378564),
            ),
            'roll' : m.radians(-53.1177),
            'position_offset' : {
                'wrist_newbonehead_to_wrist_mcp_ratio' : 0.340676714289, # Multiply this by bone the length to get the bone distance from the hand bone head
                'newbonehead_mcp_to_wrist_mcp_ratio': 0.6648740969834,
                'rotation' : ( # Rotation of the vector (0, 0, (hand_head to bone head)) to get the new bone head position
                    m.radians(125.2139785063952),
                    m.radians(24.4998970905722),
                    m.radians(45.46665685180728),
                )
            }
        },
        'f_middle.01.L': {
            'rotation' : (
                # m.radians(153.59596899854776),
                # m.radians(2.9706012417475782),
                # m.radians(12.614850547920385),
                m.radians(143.08130258266334),
                m.radians(13.012718458583736),
                m.radians(37.726389371119936),
            ),
            'roll' : m.radians(-5.37182)
        },
        'f_middle.02.L': {
            'rotation' : (
                # m.radians(-12.509869686603643),
                # m.radians(-161.1841315815135),
                # m.radians(66.96937643457139),
                m.radians(149.94827915154576),
                m.radians(-5.78780881445454),
                m.radians(-21.33001141941116),
            ),
            'roll' : m.radians(29.932)
        },
        'f_middle.03.L': {
            'rotation' : (
                # m.radians(-12.509869686603643),
                # m.radians(-161.1841315815135),
                # m.radians(66.96937643457139),
                m.radians(151.32890626961546),
                m.radians(-9.54644185103187),
                m.radians(-36.1888830530988),
            ),
            'roll' : m.radians(36.1311)
        },
        'palm.03.R': {
            'rotation' : (
                m.radians(-35.38173227812171),
                m.radians(-144.13648484716026),
                m.radians(89.17283244504377),
            ),
            'roll' : m.radians(-158.0)
        },
        'f_ring.01.R': {
            'rotation' : (
                m.radians(157.3626134201347),
                m.radians(-10.553912682855323),
                m.radians(-49.541062767205815),
            ),
            'roll' : m.radians(-175.0)
        },
        'f_ring.02.R': {
            'rotation' : (
                m.radians(166.01302068319916),
                m.radians(5.336361484847024),
                m.radians(41.603730668585264),
            ),
            'roll' : m.radians(151.0)
        },
        'f_ring.03.R': {
            'rotation' : (
                m.radians(166.01302068319916),
                m.radians(5.336361484847024),
                m.radians(41.603730668585264),
            ),
            'roll' : m.radians(151.0)
        },
        'palm.03.L': {
            'rotation' : (
                # m.radians(-35.38086484409712),
                # m.radians(144.13655314905196),
                # m.radians(-89.17146640720976),
                m.radians(-32.238001108839946),
                m.radians(145.70458699756847),
                m.radians(-86.25082287659896),
            ),
            'roll' : m.radians(-44.5467),
            'position_offset' : {
                'wrist_newbonehead_to_wrist_mcp_ratio' : 0.35884854835727, # Multiply this by bone the length to get the bone distance from the hand bone head
                'newbonehead_mcp_to_wrist_mcp_ratio': 0.6418171731492,
                'rotation' : ( # Rotation of the vector (0, 0, (hand_head to bone head)) to get the new bone head position
                    m.radians(-27.89104503234851),
                    m.radians(148.06956731844207),
                    m.radians(-81.91446554615209),
                )
            }
        },
        'f_ring.01.L': {
            'rotation' : (
                # m.radians(158.7280911786253),
                # m.radians(-1.3540651527177525),
                # m.radians(-7.201199923085966),
                m.radians(152.20705003082566),
                m.radians(16.741936004839935),
                m.radians(61.48498724805043),
            ),
            'roll' : m.radians(-15.4552)
        },
        'f_ring.02.L': {
            'rotation' : (
                # m.radians(163.8374688287667),
                # m.radians(-9.297557441639421),
                # m.radians(-59.59876903704888),
                m.radians(157.27711311210447),
                m.radians(-7.749905731379879),
                m.radians(-37.257274903450536),
            ),
            'roll' : m.radians(23.1766)
        },
        'f_ring.03.L': {
            'rotation' : (
                # m.radians(163.8374688287667),
                # m.radians(-9.297557441639421),
                # m.radians(-59.59876903704888),
                m.radians(158.30196933668654),
                m.radians(-12.647343465349428),
                m.radians(-60.07702571292234),
            ),
            'roll' : m.radians(30.2891)
        },
        'palm.04.R': {
            'rotation' : (
                m.radians(-22.97185570719341),
                m.radians(-145.80376134431705),
                m.radians(66.89572650475114),
            ),
            'roll' : m.radians(-157.0)
        },
        'f_pinky.01.R': {
            'rotation' : (
                m.radians(163.10432998363586),
                m.radians(-13.879361888778927),
                m.radians(-78.67092482252893),
            ),
            'roll' : m.radians(-170.0)
        },
        'f_pinky.02.R': {
            'rotation' : (
                m.radians(168.97607968855576),
                m.radians(4.6775274139231175),
                m.radians(45.879312975797355),
            ),
            'roll' : m.radians(-95.0)
        },
        'f_pinky.03.R': {
            'rotation' : (
                m.radians(162.22981988306412),
                m.radians(2.758289507152786),
                m.radians(17.509948088325558),
            ),
            'roll' : m.radians(-80.0)
        },
        'palm.04.L': {
            'rotation' : (
                # m.radians(-22.97141174489736),
                # m.radians(145.80314662729177),
                # m.radians(-66.8936842781893),
                m.radians(-20.033393920585326),
                m.radians(154.91997384839806),
                m.radians(-76.90547801643154),
            ),
            'roll' : m.radians(-32.1242),
            'position_offset' : {
                'wrist_newbonehead_to_wrist_mcp_ratio' : 0.4207464081, # Multiply this by bone the length to get the bone distance from the hand bone head
                'newbonehead_mcp_to_wrist_mcp_ratio': 0.5927105884668,
                'rotation' : ( # Rotation of the vector (0, 0, (hand_head to bone head)) to get the new bone head position
                    m.radians(0.6279726082111441),
                    m.radians(149.8150085004605),
                    m.radians(2.328285556444525),
                )
            }
        },
        'f_pinky.01.L': {
            'rotation' : (
                # m.radians(164.59784646830755),
                # m.radians(6.764079769036197),
                # m.radians(47.212989373512386),
                m.radians(160.63697878748212),
                m.radians(13.096721247638431),
                m.radians(67.87011446155599),
            ),
            'roll' : m.radians(-15.4837)
        },
        'f_pinky.02.L': {
            'rotation' : (
                # m.radians(-9.264448953411431),
                # m.radians(-169.27331586085637),
                # m.radians(81.59100144743863),
                m.radians(161.64317493525172),
                m.radians(-6.878367189983905),
                m.radians(-40.8043184979378),
            ),
            'roll' : m.radians(12.3853)
        },
        'f_pinky.03.L': {
            'rotation' : (
                # m.radians(163.6619739482324),
                # m.radians(-9.964792645242444),
                # m.radians(-62.541241852247055),
                m.radians(161.84663261024807),
                m.radians(-10.873213781269664),
                m.radians(-61.56738665019747),
            ),
            'roll' : m.radians(17.8652)
        },
        'thigh.R': {
            'rotation' : (
                m.radians(1),
                m.radians(-176.63197042733134),
                m.radians(4.106872792731369),
            ),
            'roll': m.radians(101),
        },
        'thigh.L': {
            'rotation' : (
                m.radians(1),
                m.radians(176.63197042733134),
                m.radians(-4.106635016770888),
            ),
            'roll': m.radians(-101),
        },
        'shin.R': {
            'rotation' : (
                m.radians(-175.12260790378525),
                m.radians(-2.6481038282450826),
                m.radians(56.97761905625937),
            ),
            'roll': m.radians(101),
        },
        'shin.L': {
            'rotation' : (
                m.radians(-175.12259424340692),
                m.radians(2.648141394285518),
                m.radians(-56.97820303743341),
            ),
            'roll': m.radians(-101),
        },
        'foot.R': {
            'rotation' : (
                m.radians(106.8930615673465),
                m.radians(-8.188085418524645),
                m.radians(-11.028648396211644),
            ),
            'roll': m.radians(90),
        },
        'foot.L': {
            'rotation' : (
                m.radians(107.86645231653254),
                m.radians(8.93590490150277),
                m.radians(12.247207078107985),
            ),
            'roll': m.radians(-90),
        },
        'heel.02.R': {
            'rotation' : (
                m.radians(195),
                0,
                0
            ),
            'roll': 0,
        },
        'heel.02.L': {
            'rotation' : (
                m.radians(195),
                0,
                0
            ),
            'roll': 0,
        },
    }
}