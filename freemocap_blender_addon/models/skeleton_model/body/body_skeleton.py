from freemocap_blender_addon.models.skeleton_model.body.chains.axial_body_chain import AxialBodyChain
from freemocap_blender_addon.models.skeleton_model.body.chains.left_body_chains import LeftArmChain, LeftLegChain
from freemocap_blender_addon.models.skeleton_model.body.chains.right_body_chains import RightArmChain, RightLegChain
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC


class BodySkeletonDefinition(SkeletonABC):
    parent = AxialBodyChain
    children = [RightArmChain,
                RightLegChain,
                LeftArmChain,
                LeftLegChain]




