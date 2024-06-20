from skelly_blender.core.blender_stuff.blenderizers.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_linkages import BodyLinkages


class AxialBodyChain(ChainABC):
    parent = BodyLinkages.CHEST_T12.value
    children = [BodyLinkages.NECK_C7.value,
                BodyLinkages.SKULL_C1.value
                ]


class LeftArmChain(ChainABC):
    parent = BodyLinkages.LEFT_SHOULDER.value
    children = [BodyLinkages.LEFT_ELBOW.value,
                BodyLinkages.LEFT_WRIST.value,
                ]


class LeftLegChain(ChainABC):
    parent = BodyLinkages.LEFT_HIP.value
    children = [BodyLinkages.LEFT_KNEE.value,
                BodyLinkages.LEFT_ANKLE.value,
                ]


class RightArmChain(ChainABC):
    parent = BodyLinkages.RIGHT_SHOULDER.value
    children = [BodyLinkages.RIGHT_ELBOW.value,
                BodyLinkages.RIGHT_WRIST.value,
                ]


class RightLegChain(ChainABC):
    parent = BodyLinkages.RIGHT_HIP.value
    children = [BodyLinkages.RIGHT_KNEE.value,
                BodyLinkages.RIGHT_ANKLE.value,
                ]

class BodyChains(BlenderizableEnum):
    AXIAL = AxialBodyChain
    RIGHT_ARM = RightArmChain
    RIGHT_LEG = RightLegChain
    LEFT_ARM = LeftArmChain
    LEFT_LEG = LeftLegChain
