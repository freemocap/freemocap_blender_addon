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
                m.radians(134.3696695039),
                m.radians(-30.2726517412),
                m.radians(-65.4836463656),
            ),
            'roll': m.radians(-135.9674829772),           
        },
        'hand.L': {
            'rotation' : (
                m.radians(134.37488776840476),
                m.radians(30.27156232603659),
                m.radians(65.48831821494582),
            ),
            'roll': m.radians(135.9672),
        },
        'palm.01.R': {
            'rotation': (m.radians(116.2904046577), m.radians(-20.5056144168), m.radians(-32.4613551249)),
            'roll': m.radians(-142.9584001587),
        },
        'palm.02.R': {
            'rotation': (m.radians(129.4675607743), m.radians(-31.5157564154), m.radians(-61.7473211537)),
            'roll': m.radians(-126.8825527395),
        },
        'palm.03.R': {
            'rotation': (m.radians(-30.8289945548), m.radians(-145.9700218091), m.radians(84.0370970949)),
            'roll': m.radians(-135.4534839214),
        },
        'palm.04.R': {
            'rotation': (m.radians(-10.0434269056), m.radians(-150.4173355626), m.radians(36.8128754753)),
            'roll': m.radians(-147.8759451159),
        },
        'thumb.carpal.R': {
            'rotation': (m.radians(95.4501246319), m.radians(28.1864302234), m.radians(30.8750163694)),
            'roll': m.radians(118.0000000000),
        },
        'thumb.01.R': {
            'rotation': (m.radians(111.2203962179), m.radians(2.7832382672), m.radians(4.0654626365)),
            'roll': m.radians(63.1381594046),
        },
        'thumb.02.R': {
            'rotation': (m.radians(130.7684795847), m.radians(-1.4829530635), m.radians(-3.2360172703)),
            'roll': m.radians(81.6832841333),
        },
        'thumb.03.R': {
            'rotation': (m.radians(147.1136277026), m.radians(0.0000000000), m.radians(0.0000000000)),
            'roll': m.radians(-82.1634464320),
        },
        'f_index.01.R': {
            'rotation': (m.radians(139.3898722042), m.radians(-10.7934636387), m.radians(-28.6452123224)),
            'roll': m.radians(172.8830298561),
        },
        'f_index.02.R': {
            'rotation': (m.radians(145.4178419958), m.radians(-0.3960912611), m.radians(-1.2723533585)),
            'roll': m.radians(151.0099227750),
        },
        'f_index.03.R': {
            'rotation': (m.radians(147.4322970085), m.radians(3.0745699544), m.radians(10.4982731081)),
            'roll': m.radians(144.5941075216),
        },
        'f_middle.01.R': {
            'rotation': (m.radians(143.0871765453), m.radians(-13.0114292604), m.radians(-37.7288618996)),
            'roll': m.radians(-174.6284710381),
        },
        'f_middle.02.R': {
            'rotation': (m.radians(149.9462710759), m.radians(5.7885554395), m.radians(21.3312442686)),
            'roll': m.radians(150.0678074620),
        },
        'f_middle.03.R': {
            'rotation': (m.radians(151.3468286860), m.radians(0.0000000000), m.radians(0.0000000000)),
            'roll': m.radians(143.8686731298),
        },
        'f_ring.01.R': {
            'rotation': (m.radians(152.2042769740), m.radians(-16.7426685426), m.radians(-61.4820024554)),
            'roll': m.radians(-164.5449944645),
        },
        'f_ring.02.R': {
            'rotation': (m.radians(157.2786840556), m.radians(7.7493746842), m.radians(37.2573466204)),
            'roll': m.radians(156.8232197210),
        },
        'f_ring.03.R': {
            'rotation': (m.radians(155.2617838352), m.radians(13.2895665162), m.radians(55.9562906244)),
            'roll': m.radians(152.8232287166),
        },
        'f_pinky.01.R': {
            'rotation': (m.radians(160.6376891272), m.radians(-13.0974913515), m.radians(-67.8752507638)),
            'roll': m.radians(-164.5164852549),
        },
        'f_pinky.02.R': {
            'rotation': (m.radians(161.6392407463), m.radians(6.8813652161), m.radians(40.8125283853)),
            'roll': m.radians(167.6145224586),
        },
        'f_pinky.03.R': {
            'rotation': (m.radians(161.8598421961), m.radians(10.8664979978), m.radians(61.5733494053)),
            'roll': m.radians(162.1346207064),
        },

        'palm.01.L': {
            'rotation': (m.radians(116.2904046577), m.radians(20.5056144168), m.radians(32.4613551249)),
            'roll': m.radians(142.9584001587),
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
        'palm.02.L': {
            'rotation': (m.radians(129.4675607743), m.radians(31.5157564154), m.radians(61.7473211537)),
            'roll': m.radians(126.8825527395),
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
        'palm.03.L': {
            'rotation': (m.radians(-30.8289945548), m.radians(145.9700218091), m.radians(-84.0370970949)),
            'roll': m.radians(135.4534839214),
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
        'palm.04.L': {
            'rotation': (m.radians(-10.0434269056), m.radians(150.4173355626), m.radians(-36.8128754753)),
            'roll': m.radians(147.8759451159),
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
        'thumb.carpal.L': {
            'rotation': (m.radians(95.4501246319), m.radians(-28.1864302234), m.radians(-30.8750163694)),
            'roll': m.radians(-118.0000000000),
        },
        'thumb.01.L': {
            'rotation': (m.radians(111.2203962179), m.radians(-2.7832382672), m.radians(-4.0654626365)),
            'roll': m.radians(-63.1381594046),
        },
        'thumb.02.L': {
            'rotation': (m.radians(130.7684795847), m.radians(1.4829530635), m.radians(3.2360172703)),
            'roll': m.radians(-81.6832841333),
        },
        'thumb.03.L': {
            'rotation': (m.radians(147.1136277026), m.radians(0.0000000000), m.radians(0.0000000000)),
            'roll': m.radians(82.1634464320),
        },
        'f_index.01.L': {
            'rotation': (m.radians(139.3898722042), m.radians(10.7934636387), m.radians(28.6452123224)),
            'roll': m.radians(-172.8830298561),
        },
        'f_index.02.L': {
            'rotation': (m.radians(145.4178419958), m.radians(0.3960912611), m.radians(1.2723533585)),
            'roll': m.radians(-151.0099227750),
        },
        'f_index.03.L': {
            'rotation': (m.radians(147.4322970085), m.radians(-3.0745699544), m.radians(-10.4982731081)),
            'roll': m.radians(-144.5941075216),
        },
        'f_middle.01.L': {
            'rotation': (m.radians(143.0871765453), m.radians(13.0114292604), m.radians(37.7288618996)),
            'roll': m.radians(174.6284710381),
        },
        'f_middle.02.L': {
            'rotation': (m.radians(149.9462710759), m.radians(-5.7885554395), m.radians(-21.3312442686)),
            'roll': m.radians(-150.0678074620),
        },
        'f_middle.03.L': {
            'rotation': (m.radians(151.3468286860), m.radians(0.0000000000), m.radians(0.0000000000)),
            'roll': m.radians(-143.8686731298),
        },
        'f_ring.01.L': {
            'rotation': (m.radians(152.2042769740), m.radians(16.7426685426), m.radians(61.4820024554)),
            'roll': m.radians(164.5449944645),
        },
        'f_ring.02.L': {
            'rotation': (m.radians(157.2786840556), m.radians(-7.7493746842), m.radians(-37.2573466204)),
            'roll': m.radians(-156.8232197210),
        },
        'f_ring.03.L': {
            'rotation': (m.radians(155.2617838352), m.radians(-13.2895665162), m.radians(-55.9562906244)),
            'roll': m.radians(-152.8232287166),
        },
        'f_pinky.01.L': {
            'rotation': (m.radians(160.6376891272), m.radians(13.0974913515), m.radians(67.8752507638)),
            'roll': m.radians(164.5164852549),
        },
        'f_pinky.02.L': {
            'rotation': (m.radians(161.6392407463), m.radians(-6.8813652161), m.radians(-40.8125283853)),
            'roll': m.radians(-167.6145224586),
        },
        'f_pinky.03.L': {
            'rotation': (m.radians(161.8598421961), m.radians(-10.8664979978), m.radians(-61.5733494053)),
            'roll': m.radians(-162.1346207064),
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
        'spine.001': { # chestLower
            'rotation': (
                m.radians(-34.2140909489),
                m.radians(0.0000000000),
                m.radians(0.0000000000),
            ),
            'roll': m.radians(0.0000000000),
        },
        'neck': { # neckUpper
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
                # m.radians(-97.4433036053),
                m.radians(-91.8433036053), # To compensate for the longer spine.001 bone
                m.radians(-35.1954456987),
            ),
            'roll': m.radians(-95.5465259219),
        },
        'shoulder.L': {
            'rotation': (
                m.radians(31.1179661982),
                # m.radians(97.4432694544),
                m.radians(91.8432694544), # To compensate for the longer spine.001 bone
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
            # 'roll': m.radians(-45.8334448404),
            'roll': m.radians(134.1665551596),
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
            # 'roll': m.radians(-46.6059289903),
            'roll': m.radians(133.3940452828),
        },
        'thumb.carpal.R': {
            'rotation': (
                m.radians(133.7236838726),
                m.radians(-13.0736667979),
                m.radians(-30.0214817798),
            ),
            'roll': m.radians(0.0000000000),
        },
        'thumb.carpal.L': {
            'rotation': (
                m.radians(133.7236838726),
                m.radians(13.0736667979),
                m.radians(30.0214817798),
            ),
            'roll': m.radians(0.0000000000),
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