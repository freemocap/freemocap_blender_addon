from freemocap_blender_addon.models.skeleton.abstract_base_classes import SkeletonABC
from freemocap_blender_addon.models.skeleton.body.c_linkages.axial_body_linkages import PelvisSacrumLinkage, \
    ChestT1Linkage, NeckC1Linkage, SkullC1Linkage, NeckC7Linkage


class FullBodySkeleton(SkeletonABC):
    parent = PelvisSacrumLinkage
    children = [ChestT1Linkage,
                NeckC1Linkage,
                NeckC7Linkage,
                SkullC1Linkage]