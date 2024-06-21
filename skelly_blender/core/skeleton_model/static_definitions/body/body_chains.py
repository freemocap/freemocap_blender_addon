from skelly_blender.core.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from skelly_blender.core.skeleton_model.abstract_base_classes.base_enums import ChainEnum
from skelly_blender.core.skeleton_model.static_definitions.body.body_linkages import BodyLinkages


class AxialBodyChain(ChainABC):
    parent = BodyLinkages.CHEST_T12
    children = [BodyLinkages.NECK_C7,
                BodyLinkages.SKULL_C1
                ]


class LeftArmChain(ChainABC):
    parent = BodyLinkages.LEFT_SHOULDER
    children = [BodyLinkages.LEFT_ELBOW,
                BodyLinkages.LEFT_WRIST,
                ]


class LeftLegChain(ChainABC):
    parent = BodyLinkages.LEFT_HIP
    children = [BodyLinkages.LEFT_KNEE,
                BodyLinkages.LEFT_ANKLE,
                ]


class RightArmChain(ChainABC):
    parent = BodyLinkages.RIGHT_SHOULDER
    children = [BodyLinkages.RIGHT_ELBOW,
                BodyLinkages.RIGHT_WRIST,
                ]


class RightLegChain(ChainABC):
    parent = BodyLinkages.RIGHT_HIP
    children = [BodyLinkages.RIGHT_KNEE,
                BodyLinkages.RIGHT_ANKLE,
                ]

class BodyChains(ChainEnum):
    AXIAL = AxialBodyChain
    RIGHT_ARM = RightArmChain
    RIGHT_LEG = RightLegChain
    LEFT_ARM = LeftArmChain
    LEFT_LEG = LeftLegChain
