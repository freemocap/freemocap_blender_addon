from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.chains.axial_body_chain import AxialBodyChain
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.chains.left_body_chains import LeftArmChain, \
    LeftLegChain
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.chains.right_body_chains import RightArmChain, \
    RightLegChain


class BodySkeletonDefinition(SkeletonABC):
    parent = AxialBodyChain
    children = [RightArmChain,
                RightLegChain,
                LeftArmChain,
                LeftLegChain]
