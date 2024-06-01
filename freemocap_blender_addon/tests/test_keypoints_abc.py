from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints_abc import Keypoints


class ExampleKeypoints(Keypoints):
    RIGHTLEFT_EYE = auto()
    NOSE = auto()
    RIGHTLEFT_HAND = auto()
    MOUTH = auto()


def test_keypoint_creation():
    # Test that keypoints are created correctly and names are converted to lowercase
    assert ExampleKeypoints.RIGHT_EYE.value.name == 'right_eye'
    assert ExampleKeypoints.LEFT_EYE.value.name == 'left_eye'
    assert ExampleKeypoints.NOSE.value.name == 'nose'
    assert ExampleKeypoints.MOUTH.value.name == 'mouth'


def test_to_list():
    # Test that all keypoints are returned correctly
    expected_keypoints = ['righteye_left', 'righteye_right', 'nose', 'righthand_left', 'righthand_right', 'mouth']
    keypoints_list = ExampleKeypoints.to_list()
    keypoints_names = [kp.name for kp in keypoints_list]
    assert set(keypoints_names) == set(expected_keypoints)


def test_to_list_with_exclusion():
    # Test that excluded keypoints are not in the list
    excluded_keypoints = [ExampleKeypoints.NOSE]
    expected_keypoints = ['righteye_left', 'righteye_right', 'righthand_left', 'righthand_right', 'mouth']
    keypoints_list = ExampleKeypoints.to_list(excluded=[kp.value.name for kp in excluded_keypoints])
    keypoints_names = [kp.name for kp in keypoints_list]
    assert set(keypoints_names) == set(expected_keypoints)


def test_to_list_with_multiple_exclusions():
    # Test that multiple excluded keypoints are not in the list
    excluded_keypoints = [ExampleKeypoints.NOSE, ExampleKeypoints.MOUTH]
    expected_keypoints = ['righteye_left', 'righteye_right', 'righthand_left', 'righthand_right']
    keypoints_list = ExampleKeypoints.to_list(excluded=[kp.value.name for kp in excluded_keypoints])
    keypoints_names = [kp.name for kp in keypoints_list]
    assert set(keypoints_names) == set(expected_keypoints)


def test_to_list_with_no_exclusions():
    # Test that all keypoints are returned when no exclusions are provided
    expected_keypoints = ['righteye_left', 'righteye_right', 'nose', 'righthand_left', 'righthand_right', 'mouth']
    keypoints_list = ExampleKeypoints.to_list()
    keypoints_names = [kp.name for kp in keypoints_list]
    assert set(keypoints_names) == set(expected_keypoints)