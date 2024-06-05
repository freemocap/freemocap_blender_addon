from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import SimpleRigidBodyABC, CompoundRigidBodyABC
from freemocap_blender_addon.models.skeleton.body.a_keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.body.a_keypoints.right_body_keypoints import RightBodyKeypoints


#arm
class RightClavicleRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.CHEST_T1_CENTER.value
    child = RightBodyKeypoints.RIGHT_SHOULDER.value


class RightUpperArmRigidBody(SimpleRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_SHOULDER.value
    child = RightBodyKeypoints.RIGHT_ELBOW.value


class RightForearmRigidBody(SimpleRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_ELBOW.value
    child = RightBodyKeypoints.RIGHT_WRIST.value


class RightPalmRigidBody(CompoundRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_WRIST.value
    children = [
        RightBodyKeypoints.RIGHT_INDEX_KNUCKLE.value,
        RightBodyKeypoints.RIGHT_PINKY_KNUCKLE.value,
    ]

class RightIndexMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_WRIST.value
    child = RightBodyKeypoints.RIGHT_INDEX_KNUCKLE.value



class RightThumbRigidBody(CompoundRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_WRIST.value
    children = [
        RightBodyKeypoints.RIGHT_INDEX_KNUCKLE.value,
        RightBodyKeypoints.RIGHT_PINKY_KNUCKLE.value,
    ]


#leg
class RightPelvisRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.PELVIS_SACRUM.value
    child = RightBodyKeypoints.RIGHT_HIP.value


class RightThighRigidBody(SimpleRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_HIP.value
    child = RightBodyKeypoints.RIGHT_KNEE.value


class RightCalfRigidBody(SimpleRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_KNEE.value
    child = RightBodyKeypoints.RIGHT_ANKLE.value


class RightFootRigidBody(CompoundRigidBodyABC):
    parent = RightBodyKeypoints.RIGHT_ANKLE.value
    children = [
        RightBodyKeypoints.RIGHT_HEEL.value,
        RightBodyKeypoints.RIGHT_HALLUX_TIP.value
    ]
