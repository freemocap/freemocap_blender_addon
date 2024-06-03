from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightBodyKeypoints
from freemocap_blender_addon.models.skeleton.rigid_bodies.right_rigid_bodies import RightUpperArmRigidBody, \
    RightClavicleRigidBody, RightForearmRigidBody, RightPalmRigidBody


class RightShoulderLinkage(LinkageABC):
    bodies = [RightClavicleRigidBody, RightUpperArmRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_SHOULDER.value


class RightElbowLinkage(LinkageABC):
    bodies = [RightUpperArmRigidBody, RightForearmRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_ELBOW.value


class RightWristLinkage(LinkageABC):
    bodies = [RightForearmRigidBody,
              RightPalmRigidBody,
              ]
    linked_keypoint = RightBodyKeypoints.RIGHT_WRIST.value
