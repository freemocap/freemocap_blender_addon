from freemocap_blender_addon.models.skeleton.abstract_base_classes import LinkageABC
from freemocap_blender_addon.models.skeleton.body.a_keypoints.left_body_keypoints import LeftBodyKeypoints
from freemocap_blender_addon.models.skeleton.body.b_rigid_bodies.left_body_rigid_bodies import LeftThumbRigidBody, \
    LeftClavicleRigidBody, LeftUpperArmRigidBody, LeftForearmRigidBody, LeftPalmRigidBody


class LeftShoulderLinkage(LinkageABC):
    bodies = [LeftClavicleRigidBody,
              LeftUpperArmRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_SHOULDER.value


class LeftElbowLinkage(LinkageABC):
    bodies = [LeftUpperArmRigidBody,
              LeftForearmRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_ELBOW.value


class LeftWristLinkage(LinkageABC):
    bodies = [LeftForearmRigidBody,
              LeftPalmRigidBody,
              LeftThumbRigidBody,
              ]
    linked_keypoint = LeftBodyKeypoints.LEFT_WRIST.value
