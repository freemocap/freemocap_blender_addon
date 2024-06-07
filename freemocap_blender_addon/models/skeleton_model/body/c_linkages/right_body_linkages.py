from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import LinkageABC
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.right_body_keypoints import RightBodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.rigid_bodies.right_body_rigid_bodies import RightUpperArmRigidBody, \
    RightClavicleRigidBody, RightForearmRigidBody, RightPalmRigidBody, RightThumbRigidBody, RightPelvisRigidBody, \
    RightThighRigidBody, RightCalfRigidBody, RightFootRigidBody


class RightShoulderLinkage(LinkageABC):
    bodies = [RightClavicleRigidBody,
              RightUpperArmRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_SHOULDER.value


class RightElbowLinkage(LinkageABC):
    bodies = [RightUpperArmRigidBody,
              RightForearmRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_ELBOW.value


class RightWristLinkage(LinkageABC):
    bodies = [RightForearmRigidBody,
              RightPalmRigidBody,
              RightThumbRigidBody,
              ]
    linked_keypoint = RightBodyKeypoints.RIGHT_WRIST.value

class RightHipLinkage(LinkageABC):
    bodies = [RightPelvisRigidBody,
              RightThighRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_HIP.value

class RightKneeLinkage(LinkageABC):
    bodies = [RightThighRigidBody,
              RightCalfRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_KNEE.value

class RightAnkleLinkage(LinkageABC):
    bodies = [RightCalfRigidBody,
              RightFootRigidBody]
    linked_keypoint = RightBodyKeypoints.RIGHT_ANKLE.value