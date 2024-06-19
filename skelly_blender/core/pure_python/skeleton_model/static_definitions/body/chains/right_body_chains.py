from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.linkages.right_body_linkages import \
    RightShoulderLinkage, RightElbowLinkage, RightWristLinkage, RightAnkleLinkage, RightHipLinkage, RightKneeLinkage


class RightArmChain(ChainABC):
    parent = RightShoulderLinkage
    children = [RightElbowLinkage,
                RightWristLinkage,
                ]


class RightLegChain(ChainABC):
    parent = RightHipLinkage
    children = [RightKneeLinkage,
                RightAnkleLinkage,
                ]
