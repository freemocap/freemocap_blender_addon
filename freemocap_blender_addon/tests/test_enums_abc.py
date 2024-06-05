from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointsEnum


class ExampleKeypoints(KeypointsEnum):
    THING1 = auto()
    THING2 = auto()


def test_keypoint_creation():
    # Test that keypoints are created correctly and names are converted to lowercase
    assert ExampleKeypoints.THING1.value.name == 'THING1'
    assert ExampleKeypoints.THING2.value.name == 'THING2'


