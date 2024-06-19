from skelly_blender.core.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from skelly_blender.core.skeleton_model.static_definitions.body.linkages.left_body_linkages import LeftShoulderLinkage, \
    LeftWristLinkage, LeftElbowLinkage, LeftAnkleLinkage, LeftKneeLinkage, LeftHipLinkage


class LeftArmChain(ChainABC):
    parent = LeftShoulderLinkage
    children = [LeftElbowLinkage,
                LeftWristLinkage,
                ]


class LeftLegChain(ChainABC):
    parent = LeftHipLinkage
    children = [LeftKneeLinkage,
                LeftAnkleLinkage,
                ]
