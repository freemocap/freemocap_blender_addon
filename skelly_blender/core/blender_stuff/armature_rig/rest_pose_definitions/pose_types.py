from enum import Enum

from skelly_blender.core.blender_stuff.armature_rig.rest_pose_definitions.default_body_tpose import \
    BodyArmatureTPoseDefinition

_REST_POSE_TYPES = {
    "DEFAULT_TPOSE": BodyArmatureTPoseDefinition
}
RestPoseTypes = Enum("RestPoseTypes", _REST_POSE_TYPES)
