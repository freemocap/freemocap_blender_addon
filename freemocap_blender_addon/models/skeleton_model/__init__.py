from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_skeleton import BodySkeletonDefinition
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.skeleton_abc import SkeletonABC


class SkeletonTypes(Enum):
    BODY_ONLY: SkeletonABC = BodySkeletonDefinition
