from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_chains import BodyChains


class BodySkeletonDefinition(SkeletonABC):
    parent = BodyChains.AXIAL
    children = [BodyChains.RIGHT_ARM,
                BodyChains.RIGHT_LEG,
                BodyChains.LEFT_ARM,
                BodyChains.LEFT_LEG,
                ]
