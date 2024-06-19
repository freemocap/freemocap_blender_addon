from skelly_blender.core.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from skelly_blender.core.skeleton_model.static_definitions.body.linkages.axial_body_linkages import ChestT12Linkage, \
    SkullC1Linkage, NeckC7Linkage


class AxialBodyChain(ChainABC):
    parent = ChestT12Linkage
    children = [SkullC1Linkage,
                NeckC7Linkage,
                ]
