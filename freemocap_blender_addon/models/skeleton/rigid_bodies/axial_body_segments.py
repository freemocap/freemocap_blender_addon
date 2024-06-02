from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import CompositeRigidBody, \
    SimpleRigidBody


class SkullRigidBody(CompositeRigidBody):
    parent = AxialBodyKeypoints.SKULL_CENTER.value
    children = [AxialBodyKeypoints.NOSE.value,
                AxialBodyKeypoints.SKULL_BREGMA.value,
                AxialBodyKeypoints.RIGHT_EYE_INNER.value,
                AxialBodyKeypoints.RIGHT_EYE_CENTER.value,
                AxialBodyKeypoints.RIGHT_EYE_OUTER.value,
                AxialBodyKeypoints.RIGHT_EAR_TRAGUS.value,
                AxialBodyKeypoints.RIGHT_MOUTH_LEFT.value,
                AxialBodyKeypoints.RIGHT_MOUTH_RIGHT.value,
                AxialBodyKeypoints.RIGHT_HEAD_CENTER.value,
                AxialBodyKeypoints.LEFT_EYE_INNER.value,
                AxialBodyKeypoints.LEFT_EYE_CENTER.value,
                AxialBodyKeypoints.LEFT_EYE_OUTER.value,
                AxialBodyKeypoints.LEFT_EAR_TRAGUS.value,
                AxialBodyKeypoints.LEFT_MOUTH_LEFT.value,
                AxialBodyKeypoints.LEFT_MOUTH_RIGHT.value]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(AxialBodyKeypoints.NOSE.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(AxialBodyKeypoints.LEFT_EAR_TRAGUS.value)


class CervicalRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.NECK_C7.value
    child = AxialBodyKeypoints.NECK_C1.value


class ThoracicRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = AxialBodyKeypoints.NECK_C7.value


class LumbarRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = AxialBodyKeypoints.CHEST_CENTER.value
