from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightForearmSegment, \
    RightPalmSegment, RightFootSegment
from freemocap_blender_addon.models.skeleton_model.body.linkages.right_body_linkages import RightShoulderLinkage, \
    RightElbowLinkage, RightAnkleLinkage, RightKneeLinkage, RightHipLinkage


class RightArmChain(ChainABC):
    parent = RightShoulderLinkage
    children = [RightElbowLinkage,
                RightForearmSegment,
                RightPalmSegment
                ]

class RightLegChain(ChainABC):
    parent = RightHipLinkage
    children = [RightKneeLinkage,
                RightAnkleLinkage,
                RightFootSegment
                ]