from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import SkeletonABC
from freemocap_blender_addon.models.skeleton_model.body.c_linkages.axial_body_linkages import PelvisSacrumLinkage
from freemocap_blender_addon.models.skeleton_model.body.d_chains.axial_body_chain import AxialBodyChain
from freemocap_blender_addon.models.skeleton_model.body.d_chains.left_body_chains import LeftArmChain, LeftLegChain
from freemocap_blender_addon.models.skeleton_model.body.d_chains.right_body_chains import RightArmChain, RightLegChain


class FullBodySkeleton(SkeletonABC):
    parent = PelvisSacrumLinkage
    children = [AxialBodyChain,
                RightArmChain,
                RightLegChain,
                LeftArmChain,
                LeftLegChain]
