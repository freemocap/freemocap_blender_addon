from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import LinkageABC
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.left_body_keypoints import LeftBodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.b_rigid_bodies.left_body_rigid_bodies import LeftThumbRigidBody, \
    LeftClavicleRigidBody, LeftUpperArmRigidBody, LeftForearmRigidBody, LeftPalmRigidBody, LeftFootRigidBody, \
    LeftThighRigidBody, LeftPelvisRigidBody, LeftCalfRigidBody


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


class LeftHipLinkage(LinkageABC):
    bodies = [LeftPelvisRigidBody,
              LeftThighRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_HIP.value


class LeftKneeLinkage(LinkageABC):
    bodies = [LeftThighRigidBody,
              LeftCalfRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_KNEE.value


class LeftAnkleLinkage(LinkageABC):
    bodies = [LeftCalfRigidBody,
              LeftFootRigidBody]
    linked_keypoint = LeftBodyKeypoints.LEFT_ANKLE.value
