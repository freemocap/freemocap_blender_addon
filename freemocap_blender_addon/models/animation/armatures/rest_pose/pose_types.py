from enum import Enum

from freemocap_blender_addon.models.animation.armatures.rest_pose.default_body_tpose import BodyArmatureTPoseDefinition

_POSE_TYPES = {
    "DEFAULT_TPOSE": BodyArmatureTPoseDefinition
}
PoseTypes = Enum("PoseTypes", _POSE_TYPES)
