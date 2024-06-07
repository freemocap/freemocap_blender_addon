from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftForearmSegment, LeftFootSegment
from freemocap_blender_addon.models.skeleton_model.body.linkages.left_body_linkages import LeftShoulderLinkage, \
    LeftElbowLinkage, LeftAnkleLinkage, LeftKneeLinkage, LeftHipLinkage


class LeftArmChain(ChainABC):
    parent = LeftShoulderLinkage
    children = [LeftElbowLinkage,
                LeftForearmLinkage,
                LeftPalmSegment
                ]

class LeftLegChain(ChainABC):
    parent = LeftHipLinkage
    children = [LeftKneeLinkage,
                LeftAnkleLinkage,
                LeftFootSegment
                ]