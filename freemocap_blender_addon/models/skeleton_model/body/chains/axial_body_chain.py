from freemocap_blender_addon.models.skeleton_model.body.linkages.axial_body_linkages import PelvisSacrumLinkage, \
    SkullC1Linkage, NeckC7Linkage, ChestT12Linkage
from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import ChainABC


class AxialBodyChain(ChainABC):
    parent = PelvisSacrumLinkage
    children = [SkullC1Linkage,
                NeckC7Linkage,
                ChestT12Linkage,
                ]
