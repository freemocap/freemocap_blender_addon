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
                m.radians(97.93982420705119),
                m.radians(0.0),
                m.radians(0.0),
            ),
            # 'roll': m.radians(180.00000500895632),
            'roll': m.radians(0),
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
            'rotation': (
                m.radians(-81.66986964178477),
                m.radians(0.0),
                m.radians(0.0),
            ),
            'roll': m.radians(0.0),
        },
        'spine.001': {
            'rotation': (
                m.radians(-124.21377926471686),
                m.radians(0.0),
                m.radians(0.0),
            ),
            'roll': m.radians(0.0),
        },
        'neck': {
            'rotation': (
                m.radians(-58.8822480421687),
                m.radians(0.0),
                m.radians(0.0),
            ),
            'roll': m.radians(0.0),
        },
        'face': {
            'rotation': (
                m.radians(-39.2654154062314),
                m.radians(0.0),
                m.radians(0.0),
            ),
            'roll': m.radians(0.0),
        },
        'shoulder.L': {
            'rotation': (
                m.radians(-58.87267211695234),
                m.radians(97.44213564298904),
                m.radians(-65.46691923227617),
            ),
            'roll': m.radians(-176.5416070246121),
        },
        'shoulder.R': {
            'rotation': (
                m.radians(-58.87267211695234),
                m.radians(-97.44213564298904),
                m.radians(65.46691923227617),
            ),
            'roll': m.radians(-3.458391794485321),
        },
        'upper_arm.L': {
            'rotation': (
                m.radians(89.50488209154395),
                m.radians(41.8654532722964),
                m.radians(41.53607081466712),
            ),
            'roll': m.radians(178.17668601002143),
        },
        'upper_arm.R': {
            'rotation': (
                m.radians(89.50487526135477),
                m.radians(-41.8654532722964),
                m.radians(-41.5360742297617),
            ),
            'roll': m.radians(1.8233166510573766),
        },
        'forearm.L': {
            'rotation': (
                m.radians(67.75316113239785),
                m.radians(43.456381914910786),
                m.radians(29.958042982754666),
            ),
            'roll': m.radians(143.0310870318854),
        },
        'forearm.R': {
            'rotation': (
                m.radians(67.75316113239785),
                m.radians(-43.456381914910786),
                m.radians(-29.958042982754666),
            ),
            'roll': m.radians(36.96891456197635),
        },
        'hand.L': {
            'rotation': (
                m.radians(75.56505339181653),
                m.radians(58.6673907814476),
                m.radians(47.07748183547392),
            ),
            'roll': m.radians(179.87208922618032),
        },
        'hand.R': {
            'rotation': (
                m.radians(75.56505339181653),
                m.radians(-58.6673907814476),
                m.radians(-47.07748183547392),
            ),
            'roll': m.radians(0.1279174369624384),
        },
        'palm.01.L': {
            'rotation': (
                m.radians(70.31513776931295),
                m.radians(40.30687923578036),
                m.radians(28.986021686497228),
            ),
            'roll': m.radians(145.14024944758535),
        },
        'palm.01.R': {
            'rotation': (
                m.radians(70.31513776931295),
                m.radians(-40.30687923578036),
                m.radians(-28.986021686497228),
            ),
            'roll': m.radians(34.85975214627641),
        },
        'palm.02.L': {
            'rotation': (
                m.radians(81.70380885177056),
                m.radians(43.25344333429137),
                m.radians(37.84844485158806),
            ),
            'roll': m.radians(166.2270514910307),
        },
        'palm.02.R': {
            'rotation': (
                m.radians(81.70379519139222),
                m.radians(-43.25347748523722),
                m.radians(-37.84846875725016),
            ),
            'roll': m.radians(13.772947541510128),
        },
        'palm.03.L': {
            'rotation': (
                m.radians(91.11853477352696),
                m.radians(42.78162069661606),
                m.radians(43.54682727990009),
            ),
            'roll': m.radians(-175.09155786381837),
        },
        'palm.03.R': {
            'rotation': (
                m.radians(91.11853477352696),
                m.radians(-42.78162069661606),
                m.radians(-43.54682727990009),
            ),
            'roll': m.radians(-4.908438607401501),
        },
        'palm.04.L': {
            'rotation': (
                m.radians(103.5196106457097),
                m.radians(36.7321597147762),
                m.radians(45.690031358423376),
            ),
            'roll': m.radians(-151.06709145835055),
        },
        'palm.04.R': {
            'rotation': (
                m.radians(103.5196106457097),
                m.radians(-36.7321597147762),
                m.radians(-45.690031358423376),
            ),
            'roll': m.radians(-28.932906720416625),
        },
        'thumb.01.L': {
            'rotation': (
                m.radians(33.24153006773865),
                m.radians(14.441372905576024),
                m.radians(4.331762747569562),
            ),
            'roll': m.radians(32.0464108875265),
        },
        'thumb.01.R': {
            'rotation': (
                m.radians(33.241574463968256),
                m.radians(-14.44144462256231),
                m.radians(-4.3317913489867115),
            ),
            'roll': m.radians(147.95359070633523),
        },
        'thumb.02.L': {
            'rotation': (
                m.radians(56.434895639904745),
                m.radians(16.860332211460232),
                m.radians(9.093759110958228),
            ),
            'roll': m.radians(42.603222985684496),
        },
        'thumb.02.R': {
            'rotation': (
                m.radians(56.4348375832968),
                m.radians(-16.860320258629184),
                m.radians(-9.093741181711657),
            ),
            'roll': m.radians(137.39675470251515),
        },
        'thumb.03.L': {
            'rotation': (
                m.radians(43.69396321500051),
                m.radians(18.370317989768093),
                m.radians(7.418449457563854),
            ),
            'roll': m.radians(31.720617694306064),
        },
        'thumb.03.R': {
            'rotation': (
                m.radians(43.69396321500051),
                m.radians(-18.370317989768093),
                m.radians(-7.418449457563854),
            ),
            'roll': m.radians(148.2793634089882),
        },
        'f_index.01.L': {
            'rotation': (
                m.radians(79.28760894231104),
                m.radians(39.02619486074087),
                m.radians(32.72678652131898),
            ),
            'roll': m.radians(158.39025636189814),
        },
        'f_index.01.R': {
            'rotation': (
                m.radians(79.28760211212187),
                m.radians(-39.026201690930044),
                m.radians(-32.726783106224396),
            ),
            'roll': m.radians(21.609736694227156),
        },
        'f_index.02.L': {
            'rotation': (
                m.radians(83.50721784927488),
                m.radians(38.501161634336576),
                m.radians(34.62832484662887),
            ),
            'roll': m.radians(166.85889863077023),
        },
        'f_index.02.R': {
            'rotation': (
                m.radians(83.50723150965321),
                m.radians(-38.50112406829614),
                m.radians(-34.62830435606136),
            ),
            'roll': m.radians(13.141098694223297),
        },
        'f_index.03.L': {
            'rotation': (
                m.radians(84.57117690685527),
                m.radians(37.391761328208084),
                m.radians(34.21315862811882),
            ),
            'roll': m.radians(168.81123990312668),
        },
        'f_index.03.R': {
            'rotation': (
                m.radians(84.57117690685527),
                m.radians(-37.39180572443769),
                m.radians(-34.213199609253834),
            ),
            'roll': m.radians(11.188757421866852),
        },
        'f_middle.01.L': {
            'rotation': (
                m.radians(85.48554799142322),
                m.radians(42.40385317890641),
                m.radians(39.444748853079254),
            ),
            'roll': m.radians(172.3400707981921),
        },
        'f_middle.01.R': {
            'rotation': (
                m.radians(85.48556848199073),
                m.radians(-42.40385317890641),
                m.radians(-39.44476592855218),
            ),
            'roll': m.radians(7.6599205503859),
        },
        'f_middle.02.L': {
            'rotation': (
                m.radians(85.20254593335291),
                m.radians(35.96119186692725),
                m.radians(33.23525995408058),
            ),
            'roll': m.radians(169.62026214993634),
        },
        'f_middle.02.R': {
            'rotation': (
                m.radians(85.20254593335291),
                m.radians(-35.96119186692725),
                m.radians(-33.23525995408058),
            ),
            'roll': m.radians(10.379741151472706),
        },
        'f_middle.03.L': {
            'rotation': (
                m.radians(89.62202666599883),
                m.radians(42.980304069382555),
                m.radians(42.72324306977996),
            ),
            'roll': m.radians(-179.49958436922617),
        },
        'f_middle.03.R': {
            'rotation': (
                m.radians(89.62202666599883),
                m.radians(-42.980304069382555),
                m.radians(-42.72324306977996),
            ),
            'roll': m.radians(-0.5004194124305378),
        },
        'f_ring.01.L': {
            'rotation': (
                m.radians(93.9718462992998),
                m.radians(40.30804719812843),
                m.radians(42.9477923689333),
            ),
            'roll': m.radians(-169.51092448170277),
        },
        'f_ring.01.R': {
            'rotation': (
                m.radians(93.9718462992998),
                m.radians(-40.30804719812843),
                m.radians(-42.9477923689333),
            ),
            'roll': m.radians(-10.489072843290746),
        },
        'f_ring.02.L': {
            'rotation': (
                m.radians(93.1844689219699),
                m.radians(39.65217828307795),
                m.radians(41.729023658719974),
            ),
            'roll': m.radians(-169.67831875788144),
        },
        'f_ring.02.R': {
            'rotation': (
                m.radians(93.1844689219699),
                m.radians(-39.65217828307795),
                m.radians(-41.729023658719974),
            ),
            'roll': m.radians(-10.321684543527597),
        },
        'f_ring.03.L': {
            'rotation': (
                m.radians(92.19247273748475),
                m.radians(40.14798854511835),
                m.radians(41.58270051613079),
            ),
            'roll': m.radians(-174.30351795813897),
        },
        'f_ring.03.R': {
            'rotation': (
                m.radians(92.19247273748475),
                m.radians(-40.14798854511835),
                m.radians(-41.58270051613079),
            ),
            'roll': m.radians(-5.6964823550623),
        },
        'f_pinky.01.L': {
            'rotation': (
                m.radians(97.94405209414742),
                m.radians(40.72085700137483),
                m.radians(46.19584101740867),
            ),
            'roll': m.radians(-160.90383427835454),
        },
        'f_pinky.01.R': {
            'rotation': (
                m.radians(97.94409990547162),
                m.radians(-40.72085358628024),
                m.radians(-46.19587516835452),
            ),
            'roll': m.radians(-19.096167315507223),
        },
        'f_pinky.02.L': {
            'rotation': (
                m.radians(98.65848988133077),
                m.radians(40.888541560593225),
                m.radians(46.906283143927546),
            ),
            'roll': m.radians(-163.33170698110558),
        },
        'f_pinky.02.R': {
            'rotation': (
                m.radians(98.65840791906072),
                m.radians(-40.88825469264809),
                m.radians(-46.90590065333403),
            ),
            'roll': m.radians(-16.668294612756153),
        },
        'f_pinky.03.L': {
            'rotation': (
                m.radians(98.88062129351792),
                m.radians(40.620326862076),
                m.radians(46.77054679455188),
            ),
            'roll': m.radians(-165.0401421982009),
        },
        'f_pinky.03.R': {
            'rotation': (
                m.radians(98.88062812370708),
                m.radians(-40.62039857906228),
                m.radians(-46.77063217191651),
            ),
            'roll': m.radians(-14.959850857924401),
        },
        'thigh.L': {
            'rotation': (
                m.radians(92.22969726846132),
                m.radians(7.9210378285818415),
                m.radians(8.23438556336087),
            ),
            'roll': m.radians(-168.06668098170357),
        },
        'thigh.R': {
            'rotation': (
                m.radians(92.22969726846132),
                m.radians(-7.921036121034549),
                m.radians(-8.234383855813578),
            ),
            'roll': m.radians(168.06668098170357),
        },
        'shin.L': {
            'rotation': (
                m.radians(93.90165927538874),
                m.radians(8.330614391029886),
                m.radians(8.915842074589504),
            ),
            'roll': m.radians(-122.81061252238612),
        },
        'shin.R': {
            'rotation': (
                m.radians(93.90165244519957),
                m.radians(-8.330610122161655),
                m.radians(-8.915836951947627),
            ),
            'roll': m.radians(122.81061252238612),
        },
        'foot.L': {
            'rotation': (
                m.radians(144.81453138644576),
                m.radians(6.770566314313594),
                m.radians(21.134852424256387),
            ),
            'roll': m.radians(-32.07587632360594),
        },
        'foot.R': {
            'rotation': (
                m.radians(144.8145450468241),
                m.radians(-6.7706777317744296),
                m.radians(-21.135205886545933),
            ),
            'roll': m.radians(32.07587632360594),
        },
    }
}