from enum import Enum

from freemocap_blender_addon.models.animation.poses.freemocap_tpose import BodySkeletonTPoseDefinition

_POSE_TYPES = {
    "FREEMOCAP_TPOSE": BodySkeletonTPoseDefinition
}
PoseTypes = Enum("PoseTypes", _POSE_TYPES)
