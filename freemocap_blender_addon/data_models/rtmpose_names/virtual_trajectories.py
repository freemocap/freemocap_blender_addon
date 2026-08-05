"""Virtual trajectory definitions for RTMPose data.

These are computed from the BODY array only, so a definition may reference body markers.

Two differences from the MediaPipe set:

* MediaPipe's body model carries finger stubs (`right_index`, `right_pinky`), which it uses
  to synthesise `right_hand_middle`. RTMPose's body has no finger stubs - it spends those
  slots on toes and heels instead - so those definitions are omitted here. The addon builds
  the same markers separately in `add_hands_middle_empties()`, from the real hand data, which
  is a better source anyway.

* RTMPose already ships `head_center` / `neck_center` / `trunk_center` / `hips_center` as
  real trajectories. They are still listed so behaviour matches MediaPipe if a future
  RTMPose variant drops them; `calculate_virtual_trajectories` skips any name already
  present in the body data.
"""
from copy import deepcopy

_RTMPOSE_VIRTUAL_TRAJECTORY_DEFINITIONS = {
    "head_center": {
        "marker_names": ["left_ear", "right_ear"],
        "marker_weights": [0.5, 0.5],
    },
    "neck_center": {
        "marker_names": ["left_shoulder", "right_shoulder"],
        "marker_weights": [0.5, 0.5],
    },
    "trunk_center": {
        "marker_names": ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
        "marker_weights": [0.25, 0.25, 0.25, 0.25],
    },
    "hips_center": {
        "marker_names": ["left_hip", "right_hip"],
        "marker_weights": [0.5, 0.5],
    },
}


def get_rtmpose_virtual_trajectory_definition():
    """Deep copy, so callers cannot mutate the shared definition."""
    return deepcopy(_RTMPOSE_VIRTUAL_TRAJECTORY_DEFINITIONS)
