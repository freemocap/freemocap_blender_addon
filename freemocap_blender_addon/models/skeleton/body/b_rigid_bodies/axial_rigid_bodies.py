from freemocap_blender_addon.models.skeleton.body.a_keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.abstract_base_classes import CompoundRigidBodyABC, SimpleRigidBodyABC


class SkullRigidBody(CompoundRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    children = [AxialBodyKeypoints.NOSE.value,
                AxialBodyKeypoints.SKULL_BREGMA.value,
                AxialBodyKeypoints.RIGHT_EYE_INNER.value,
                AxialBodyKeypoints.RIGHT_EYE_CENTER.value,
                AxialBodyKeypoints.RIGHT_EYE_OUTER.value,
                AxialBodyKeypoints.RIGHT_EAR_TRAGUS.value,
                AxialBodyKeypoints.RIGHT_MOUTH_LEFT.value,
                AxialBodyKeypoints.RIGHT_MOUTH_RIGHT.value,
                AxialBodyKeypoints.LEFT_EYE_INNER.value,
                AxialBodyKeypoints.LEFT_EYE_CENTER.value,
                AxialBodyKeypoints.LEFT_EYE_OUTER.value,
                AxialBodyKeypoints.LEFT_EAR_TRAGUS.value,
                AxialBodyKeypoints.LEFT_MOUTH_LEFT.value,
                AxialBodyKeypoints.LEFT_MOUTH_RIGHT.value]

    shared_keypoint = AxialBodyKeypoints.SKULL_C1.value
    positive_x = AxialBodyKeypoints.NOSE.value
    approximate_positive_y = AxialBodyKeypoints.LEFT_EAR_TRAGUS.value


class CervicalRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.NECK_C7.value
    child = AxialBodyKeypoints.NECK_C1.value


class ThoracicRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.CHEST_T1_CENTER.value
    child = AxialBodyKeypoints.NECK_C7.value


class LumbarRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.PELVIS_SACRUM.value
    child = AxialBodyKeypoints.CHEST_T1_CENTER.value
