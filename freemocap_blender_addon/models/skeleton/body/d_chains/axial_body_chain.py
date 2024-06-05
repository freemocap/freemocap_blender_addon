from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton.body.c_linkages.axial_body_linkages import SkullC1Linkage, NeckC7Linkage, \
    NeckC1Linkage, ChestT1Linkage, PelvisSacrumLinkage


class AxialBodyChain(ChainABC):
    parent = PelvisSacrumLinkage
    children = [SkullC1Linkage,
                NeckC7Linkage,
                NeckC1Linkage,
                ChestT1Linkage,
                ]

