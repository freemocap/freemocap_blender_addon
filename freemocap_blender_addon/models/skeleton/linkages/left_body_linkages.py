from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import LeftBodyKeypoints
from freemocap_blender_addon.models.skeleton.linkages.abc_linkage import LinkageABC
from freemocap_blender_addon.models.skeleton.rigid_bodies.left_rigid_bodies import LeftUpperArmRigidBody, \
    LeftClavicleRigidBody, LeftForearmRigidBody, LeftPalmRigidBody


class LeftShoulderLinkage(LinkageABC):
    bodies = [LeftClavicleRigidBody, LeftUpperArmRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_SHOULDER.value


class LeftElbowLinkage(LinkageABC):
    bodies = [LeftUpperArmRigidBody, LeftForearmRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_ELBOW.value


class LeftWristLinkage(LinkageABC):
    bodies = [LeftForearmRigidBody,
              LeftPalmRigidBody,
              ]
    linked_keypoint = LeftBodyKeypoints.LEFT_WRIST.value
