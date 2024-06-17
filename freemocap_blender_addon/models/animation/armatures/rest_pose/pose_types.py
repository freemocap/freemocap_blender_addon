from enum import Enum

from freemocap_blender_addon.models.animation.armatures.rest_pose.default_body_tpose import BodyArmatureTPoseDefinition

_REST_POSE_TYPES = {
    "DEFAULT_TPOSE": BodyArmatureTPoseDefinition
}
RestPoseTypes = Enum("RestPoseTypes", _REST_POSE_TYPES)
