from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import CompoundRigidBodyABC, SimpleRigidBodyABC
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.left_body_keypoints import LeftBodyKeypoints


#arm
class LeftClavicleRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.CHEST_T1_CENTER.value
    child = LeftBodyKeypoints.LEFT_SHOULDER.value


class LeftUpperArmRigidBody(SimpleRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_SHOULDER.value
    child = LeftBodyKeypoints.LEFT_ELBOW.value


class LeftForearmRigidBody(SimpleRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_ELBOW.value
    child = LeftBodyKeypoints.LEFT_WRIST.value


class LeftPalmRigidBody(CompoundRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_WRIST.value
    children = [
        LeftBodyKeypoints.LEFT_INDEX_KNUCKLE.value,
        LeftBodyKeypoints.LEFT_PINKY_KNUCKLE.value,
    ]


class LeftThumbRigidBody(CompoundRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_WRIST.value
    children = [
        LeftBodyKeypoints.LEFT_INDEX_KNUCKLE.value,
        LeftBodyKeypoints.LEFT_PINKY_KNUCKLE.value,
    ]


#leg
class LeftPelvisRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.PELVIS_SACRUM.value
    child = LeftBodyKeypoints.LEFT_HIP.value


class LeftThighRigidBody(SimpleRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_HIP.value
    child = LeftBodyKeypoints.LEFT_KNEE.value


class LeftCalfRigidBody(SimpleRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_KNEE.value
    child = LeftBodyKeypoints.LEFT_ANKLE.value


class LeftFootRigidBody(CompoundRigidBodyABC):
    parent = LeftBodyKeypoints.LEFT_ANKLE.value
    children = [
        LeftBodyKeypoints.LEFT_HEEL.value,
        LeftBodyKeypoints.LEFT_HALLUX_TIP.value
    ]
