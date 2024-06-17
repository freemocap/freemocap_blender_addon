from freemocap_blender_addon.models.skeleton_model.body.linkages.axial_body_linkages import SkullC1Linkage, \
    NeckC7Linkage, ChestT12Linkage
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.chain_abc import ChainABC


class AxialBodyChain(ChainABC):
    parent = ChestT12Linkage
    children = [SkullC1Linkage,
                NeckC7Linkage,
                ]
