from freemocap_blender_addon.models.skeleton_model.body.linkages.right_body_linkages import RightShoulderLinkage, \
    RightElbowLinkage, RightAnkleLinkage, RightKneeLinkage, RightHipLinkage, RightWristLinkage
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.chain_abc import ChainABC


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
