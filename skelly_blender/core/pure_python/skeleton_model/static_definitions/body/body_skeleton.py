from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_chains import BodyChains


class BodySkeletonDefinition(SkeletonABC):
    parent = BodyChains.AXIAL.value
    children = [BodyChains.RIGHT_ARM.value,
                BodyChains.RIGHT_LEG.value,
                BodyChains.LEFT_ARM.value,
                BodyChains.LEFT_LEG.value,
                ]
