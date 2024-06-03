from freemocap_blender_addon.models.skeleton.abstract_base_classes import ChainABC
from freemocap_blender_addon.models.skeleton.linkages.axial_body_linkages import PelvisLinkage


class AxialBodyChain(ChainABC):
    parent = PelvisLinkage
    children = [ThoracicSpineLinkage,
                ClavicleLinkage,
                CervicalSpineLinkage,
                AtlasLinkage]