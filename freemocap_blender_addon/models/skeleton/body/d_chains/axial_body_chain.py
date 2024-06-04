from freemocap_blender_addon.models.skeleton.abstract_base_classes import ChainABC
from freemocap_blender_addon.models.skeleton.body.c_linkages.axial_body_linkages import HipsSacrumLinkage, \
    ChestT1Linkage, NeckC1Linkage, NeckC7Linkage, SkullC1Linkage, PelvisSacrumLinkage


class AxialBodyChain(ChainABC):
    parent = HipsSacrumLinkage
    children = [SkullC1Linkage,
                NeckC7Linkage,
                NeckC1Linkage,
                ChestT1Linkage,
                PelvisSacrumLinkage
                ]

