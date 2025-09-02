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
    },
    'daz_g8.1': {
        'pelvis': {
            'rotation': (
                m.radians(-21.5533654355),
                m.radians(0.0000000000),
                m.radians(0.0000000000),
            ),
            'roll': m.radians(0.0000000000),
        },
        'spine': {
            'rotation': (
                m.radians(8.3299049051),
                m.radians(0.0000000000),
                m.radians(0.0000000000),
            ),
            'roll': m.radians(0.0000000000),
        },
        'spine.001': {
            'rotation': (
                m.radians(-6.7837554096),
                m.radians(0.0000000000),
                m.radians(0.0000000000),
            ),
            'roll': m.radians(0.0000000000),
        },
        'neck': {
            'rotation': (
                m.radians(0.0000000000),
                m.radians(-0.0000000000),
                m.radians(0.0000000000),
            ),
            'roll': m.radians(0.0000000000),
        },
        'face': {
            'rotation': (
                m.radians(50.7296249658),
                m.radians(0.0000000000),
                m.radians(0.0000000000),
            ),
            'roll': m.radians(0.0000000000),
        },
        'shoulder.R': {
            'rotation': (
                m.radians(31.1178876510),
                m.radians(-97.4433036053),
                m.radians(-35.1954456987),
            ),
            'roll': m.radians(-95.5465259219),
        },
        'shoulder.L': {
            'rotation': (
                m.radians(31.1179661982),
                m.radians(97.4432694544),
                m.radians(35.1955140006),
            ),
            'roll': m.radians(-84.4534585965),
        },
        'upper_arm.R': {
            'rotation': (
                m.radians(-0.4952170494),
                m.radians(-138.1340599630),
                m.radians(1.2945621455),
            ),
            'roll': m.radians(-137.2740708446),
        },
        'upper_arm.L': {
            'rotation': (
                m.radians(-0.4952169427),
                m.radians(138.1341146046),
                m.radians(-1.2945638530),
            ),
            'roll': m.radians(-42.7259273341),
        },
        'forearm.R': {
            'rotation': (
                m.radians(-22.2467150136),
                m.radians(-136.5428307921),
                m.radians(52.5194657925),
            ),
            'roll': m.radians(-134.1665396780),
        },
        'forearm.L': {
            'rotation': (
                m.radians(-22.2467133060),
                m.radians(136.5449481507),
                m.radians(-52.5219041701),
            ),
            'roll': m.radians(-45.8334448404),
        },
        'hand.R': {
            'rotation': (
                m.radians(-14.4336121031),
                m.radians(-121.3455642662),
                m.radians(25.4039938631),
            ),
            'roll': m.radians(-133.3940452828),
        },
        'hand.L': {
            'rotation': (
                m.radians(-14.4336121031),
                m.radians(121.3464248700),
                m.radians(-25.4044258725),
            ),
            'roll': m.radians(-46.6059289903),
        },
        'palm.01.R': {
            'rotation': (
                m.radians(-19.6851755088),
                m.radians(-139.6901819616),
                m.radians(50.5997113527),
            ),
            'roll': m.radians(-140.6962278453),
        },
        'palm.02.R': {
            'rotation': (
                m.radians(-8.2969765631),
                m.radians(-136.7485151088),
                m.radians(20.7356193295),
            ),
            'roll': m.radians(-137.6994550262),
        },
        'palm.03.R': {
            'rotation': (
                m.radians(1.1174375178),
                m.radians(-137.2235547655),
                m.radians(-2.8525920080),
            ),
            'roll': m.radians(-140.0261453065),
        },
        'palm.04.R': {
            'rotation': (
                m.radians(13.5201272356),
                m.radians(-143.2676301432),
                m.radians(-39.2967284085),
            ),
            'roll': m.radians(-140.3135869876),
        },
        'palm.01.L': {
            'rotation': (
                m.radians(-19.6851755088),
                m.radians(139.6959603017),
                m.radians(-50.6066064287),
            ),
            'roll': m.radians(-39.3037703335),
        },
        'palm.02.L': {
            'rotation': (
                m.radians(-8.2969731480),
                m.radians(136.7486653729),
                m.radians(-20.7356808012),
            ),
            'roll': m.radians(-42.3005192470),
        },
        'palm.03.L': {
            'rotation': (
                m.radians(1.1174371976),
                m.radians(137.2237186901),
                m.radians(2.8526018264),
            ),
            'roll': m.radians(-39.9738357968),
        },
        'palm.04.L': {
            'rotation': (
                m.radians(13.5201323583),
                m.radians(143.2674525583),
                m.radians(39.2965576538),
            ),
            'roll': m.radians(-39.6864180214),
        },
        'thumb.01.R': {
            'rotation': (
                m.radians(123.2425127044),
                m.radians(-14.4330503201),
                m.radians(-26.3829597542),
            ),
            'roll': m.radians(-139.6529847514),
        },
        'thumb.01.L': {
            'rotation': (
                m.radians(123.2425127044),
                m.radians(14.4466765475),
                m.radians(26.4072598597),
            ),
            'roll': m.radians(-40.3467265594),
        },
        'thumb.02.R': {
            'rotation': (
                m.radians(146.4313601064),
                m.radians(-16.8681493630),
                m.radians(-52.3571053658),
            ),
            'roll': m.radians(-139.3822633735),
        },
        'thumb.02.L': {
            'rotation': (
                m.radians(146.4313601064),
                m.radians(16.8497300503),
                m.radians(52.3068317584),
            ),
            'roll': m.radians(-40.6178748242),
        },
        'thumb.03.R': {
            'rotation': (
                m.radians(133.7026195692),
                m.radians(-18.3587391116),
                m.radians(-41.4095927867),
            ),
            'roll': m.radians(-126.3646058344),
        },
        'thumb.03.L': {
            'rotation': (
                m.radians(133.7026195692),
                m.radians(18.3765659053),
                m.radians(41.4470290536),
            ),
            'roll': m.radians(-53.6354469859),
        },
        'f_index.01.R': {
            'rotation': (
                m.radians(-10.7121775574),
                m.radians(-140.9742165445),
                m.radians(29.6379495824),
            ),
            'roll': m.radians(-141.7156335789),
        },
        'f_index.01.L': {
            'rotation': (
                m.radians(-10.7121698735),
                m.radians(140.9745034124),
                m.radians(-29.6381510730),
            ),
            'roll': m.radians(-38.2843953357),
        },
        'f_index.02.R': {
            'rotation': (
                m.radians(-6.4942919926),
                m.radians(-141.5140473757),
                m.radians(18.4626365341),
            ),
            'roll': m.radians(-142.5761281313),
        },
        'f_index.02.L': {
            'rotation': (
                m.radians(-6.4942911388),
                m.radians(141.4925459402),
                m.radians(-18.4516945711),
            ),
            'roll': m.radians(-37.4238802928),
        },
        'f_index.03.R': {
            'rotation': (
                m.radians(-5.4277353287),
                m.radians(-142.6042411899),
                m.radians(15.9457852495),
            ),
            'roll': m.radians(-143.9428626446),
        },
        'f_index.03.L': {
            'rotation': (
                m.radians(-5.4277353287),
                m.radians(142.6042411899),
                m.radians(-15.9457852495),
            ),
            'roll': m.radians(-36.0570911380),
        },
        'f_middle.01.R': {
            'rotation': (
                m.radians(-4.5138466262),
                m.radians(-137.5931363015),
                m.radians(11.6015441732),
            ),
            'roll': m.radians(-138.4037568126),
        },
        'f_middle.01.L': {
            'rotation': (
                m.radians(-4.5138466262),
                m.radians(137.5931363015),
                m.radians(-11.6015441732),
            ),
            'roll': m.radians(-41.5962174605),
        },
        'f_middle.02.R': {
            'rotation': (
                m.radians(-4.7988255972),
                m.radians(-144.0251254429),
                m.radians(14.7076410002),
            ),
            'roll': m.radians(-145.4512826020),
        },
        'f_middle.02.L': {
            'rotation': (
                m.radians(-4.7988281585),
                m.radians(144.0430888404),
                m.radians(-14.7154154630),
            ),
            'roll': m.radians(-34.5487326522),
        },
        'f_middle.03.R': {
            'rotation': (
                m.radians(-0.3787976757),
                m.radians(-137.0300828271),
                m.radians(0.9623554046),
            ),
            'roll': m.radians(-138.2218278939),
        },
        'f_middle.03.L': {
            'rotation': (
                m.radians(-0.3787976490),
                m.radians(137.0134444863),
                m.radians(-0.9619455933),
            ),
            'roll': m.radians(-41.7781702849),
        },
        'f_ring.01.R': {
            'rotation': (
                m.radians(3.9736217784),
                m.radians(-139.6896492069),
                m.radians(-10.7983822287),
            ),
            'roll': m.radians(-141.8906093650),
        },
        'f_ring.01.L': {
            'rotation': (
                m.radians(3.9736204978),
                m.radians(139.6785296589),
                m.radians(10.7951566719),
            ),
            'roll': m.radians(-38.1093819835),
        },
        'f_ring.02.R': {
            'rotation': (
                m.radians(3.1820965553),
                m.radians(-140.3483799712),
                m.radians(-8.8109986708),
            ),
            'roll': m.radians(-143.8419261090),
        },
        'f_ring.02.L': {
            'rotation': (
                m.radians(3.1820967687),
                m.radians(140.3690481236),
                m.radians(8.8159642184),
            ),
            'roll': m.radians(-36.1580652396),
        },
        'f_ring.03.R': {
            'rotation': (
                m.radians(2.1939037190),
                m.radians(-139.8558960113),
                m.radians(-5.9994439334),
            ),
            'roll': m.radians(-140.9469504293),
        },
        'f_ring.03.L': {
            'rotation': (
                m.radians(2.1939030786),
                m.radians(139.8358698966),
                m.radians(5.9961944709),
            ),
            'roll': m.radians(-39.0530545797),
        },
        'f_pinky.01.R': {
            'rotation': (
                m.radians(7.9428005188),
                m.radians(-139.2757534036),
                m.radians(-21.1902930697),
            ),
            'roll': m.radians(-142.1080416071),
        },
        'f_pinky.01.L': {
            'rotation': (
                m.radians(7.9428005188),
                m.radians(139.2757534036),
                m.radians(21.1902930697),
            ),
            'roll': m.radians(-37.8918643641),
        },
        'f_pinky.02.R': {
            'rotation': (
                m.radians(8.6606491317),
                m.radians(-139.1338767141),
                m.radians(-22.9780711793),
            ),
            'roll': m.radians(-138.1881823820),
        },
        'f_pinky.02.L': {
            'rotation': (
                m.radians(8.6606465704),
                m.radians(139.1087416180),
                m.radians(22.9630754990),
            ),
            'roll': m.radians(-41.8120685137),
        },
        'f_pinky.03.R': {
            'rotation': (
                m.radians(8.8803908315),
                m.radians(-139.3745315993),
                m.radians(-23.6949832025),
            ),
            'roll': m.radians(-136.1073925721),
        },
        'f_pinky.03.L': {
            'rotation': (
                m.radians(8.8803925390),
                m.radians(139.3739168823),
                m.radians(23.6946075421),
            ),
            'roll': m.radians(-43.8925577953),
        },
        'thigh.R': {
            'rotation': (
                m.radians(2.2297297687),
                m.radians(-172.0787341002),
                m.radians(-31.3985332938),
            ),
            'roll': m.radians(27.0849631820),
        },
        'thigh.L': {
            'rotation': (
                m.radians(2.2297297687),
                m.radians(172.0787341002),
                m.radians(31.3985332938),
            ),
            'roll': m.radians(-27.0849614744),
        },
        'shin.R': {
            'rotation': (
                m.radians(3.9016512214),
                m.radians(-171.6686222216),
                m.radians(-50.1275676961),
            ),
            'roll': m.radians(0.7254352989),
        },
        'shin.L': {
            'rotation': (
                m.radians(3.9016546365),
                m.radians(171.6699199576),
                m.radians(50.1344047155),
            ),
            'roll': m.radians(-0.7254674755),
        },
        'foot.R': {
            'rotation': (
                m.radians(110.6168875330),
                m.radians(-16.7690911294),
                m.radians(-24.0406607840),
            ),
            'roll': m.radians(75.0679180731),
        },
        'foot.L': {
            'rotation': (
                m.radians(110.6169080236),
                m.radians(16.7691816294),
                m.radians(24.0407956802),
            ),
            'roll': m.radians(-75.0679180731),
        },
    },
}