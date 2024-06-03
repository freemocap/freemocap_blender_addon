from enum import auto

from freemocap_blender_addon.models.skeleton.abstract_base_classes import KeypointsABC


class ExampleKeypoints(KeypointsABC):
    THING1 = auto()
    THING2 = auto()


def test_keypoint_creation():
    # Test that keypoints are created correctly and names are converted to lowercase
    assert ExampleKeypoints.THING1.value.name == 'THING1'
    assert ExampleKeypoints.THING2.value.name == 'THING2'


