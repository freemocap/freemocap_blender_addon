from enum import Enum

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC
from freemocap_blender_addon.models.skeleton_model.body.body_skeleton import BodySkeletonDefinition


class SkeletonTypes(Enum):
    BODY_ONLY: SkeletonABC = BodySkeletonDefinition
