from enum import Enum

from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_skeleton import BodySkeletonDefinition


class SkeletonTypes(Enum):
    BODY_ONLY: SkeletonABC = BodySkeletonDefinition