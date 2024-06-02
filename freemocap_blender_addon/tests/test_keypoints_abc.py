from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import Keypoints, Keypoint


class ExampleKeypoints(Keypoints):
    THING1 = auto()
    THING2 = auto()


def test_keypoint_creation():
    # Test that keypoints are created correctly and names are converted to lowercase
    assert ExampleKeypoints.THING1.value.name == 'thing1'
    assert ExampleKeypoints.THING2.value.name == 'thing2'


def test_to_list():
    # Test that all keypoints are returned correctly
    expected_keypoints = ['thing1', 'thing2']
    keypoints_list = ExampleKeypoints.to_list()
    assert all([isinstance(kp, Keypoint) for kp in keypoints_list])
    keypoints_names = [kp.name for kp in keypoints_list]
    assert set(keypoints_names) == set(expected_keypoints)


def test_to_list_with_exclusion():
    # Test that excluded keypoints are not in the list
    excluded_keypoints = [ExampleKeypoints.THING2.value]
    expected_keypoints = [ExampleKeypoints.THING1.value]
    assert all([isinstance(kp, Keypoint) for kp in excluded_keypoints])
    keypoints_list = ExampleKeypoints.to_list(exclude=excluded_keypoints)
    assert set(expected_keypoints) == set(keypoints_list)


def test_to_list_with_multiple_exclusions():
    # Test that multiple excluded keypoints are not in the list
    excluded_keypoints = [ExampleKeypoints.THING2.value, ExampleKeypoints.THING1.value]
    expected_keypoints = []
    keypoints_list = ExampleKeypoints.to_list(exclude=excluded_keypoints)
    assert set(expected_keypoints) == set(keypoints_list)
