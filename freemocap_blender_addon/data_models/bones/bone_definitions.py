from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class BoneDefinition:
    head: str
    tail: str
    lengths: list = field(default_factory=list)
    median: float = 0.0
    stdev: float = 0.0


_BONE_DEFINITIONS: Dict[str, BoneDefinition] = {
    'pelvis.R': BoneDefinition(
        head='hips_center',
        tail='right_hip',
    ),
    'pelvis.L': BoneDefinition(
        head='hips_center',
        tail='left_hip',
    ),
    'spine': BoneDefinition(
        head='hips_center',
        tail='trunk_center',
    ),
    'spine.001': BoneDefinition(
        head='trunk_center',
        tail='neck_center',
    ),
    'neck': BoneDefinition(
        head='neck_center',
        tail='head_center',
    ),
    'head_nose': BoneDefinition(
        head='head_center',
        tail='nose',
    ),  # Auxiliary bone from head center to nose tip to align the face bones
    'shoulder.R': BoneDefinition(
        head='neck_center',
        tail='right_shoulder',
    ),
    'shoulder.L': BoneDefinition(
        head='neck_center',
        tail='left_shoulder',
    ),
    'upper_arm.R': BoneDefinition(
        head='right_shoulder',
        tail='right_elbow',
    ),
    'upper_arm.L': BoneDefinition(
        head='left_shoulder',
        tail='left_elbow',
    ),
    'forearm.R': BoneDefinition(
        head='right_elbow',
        tail='right_wrist',
    ),
    'forearm.L': BoneDefinition(
        head='left_elbow',
        tail='left_wrist',
    ),
    'hand.R': BoneDefinition(
        head='right_wrist',
        tail='right_index',
    ),
    'hand.L': BoneDefinition(
        head='left_wrist',
        tail='left_index',
    ),
    'thumb.carpal.R': BoneDefinition(
        head='right_hand_wrist',
        tail='right_hand_thumb_cmc',
    ),  # Auxiliary bone to align the right_hand_thumb_cmc empty
    'thumb.carpal.L': BoneDefinition(
        head='left_hand_wrist',
        tail='left_hand_thumb_cmc',
    ),  # Auxiliary bone to align the left_hand_thumb_cmc empty
    'thumb.01.R': BoneDefinition(
        head='right_hand_thumb_cmc',
        tail='right_hand_thumb_mcp',
    ),
    'thumb.01.L': BoneDefinition(
        head='left_hand_thumb_cmc',
        tail='left_hand_thumb_mcp',
    ),
    'thumb.02.R': BoneDefinition(
        head='right_hand_thumb_mcp',
        tail='right_hand_thumb_ip',
    ),
    'thumb.02.L': BoneDefinition(
        head='left_hand_thumb_mcp',
        tail='left_hand_thumb_ip',
    ),
    'thumb.03.R': BoneDefinition(
        head='right_hand_thumb_ip',
        tail='right_hand_thumb_tip',
    ),
    'thumb.03.L': BoneDefinition(
        head='left_hand_thumb_ip',
        tail='left_hand_thumb_tip',
    ),
    'palm.01.R': BoneDefinition(
        head='right_hand_wrist',
        tail='right_hand_index_finger_mcp',
    ),
    'palm.01.L': BoneDefinition(
        head='left_hand_wrist',
        tail='left_hand_index_finger_mcp',
    ),
    'f_index.01.R': BoneDefinition(
        head='right_hand_index_finger_mcp',
        tail='right_hand_index_finger_pip',
    ),
    'f_index.01.L': BoneDefinition(
        head='left_hand_index_finger_mcp',
        tail='left_hand_index_finger_pip',
    ),
    'f_index.02.R': BoneDefinition(
        head='right_hand_index_finger_pip',
        tail='right_hand_index_finger_dip',
    ),
    'f_index.02.L': BoneDefinition(
        head='left_hand_index_finger_pip',
        tail='left_hand_index_finger_dip',
    ),
    'f_index.03.R': BoneDefinition(
        head='right_hand_index_finger_dip',
        tail='right_hand_index_finger_tip',
    ),
    'f_index.03.L': BoneDefinition(
        head='left_hand_index_finger_dip',
        tail='left_hand_index_finger_tip',
    ),
    'palm.02.R': BoneDefinition(
        head='right_hand_wrist',
        tail='right_hand_middle_finger_mcp',
    ),
    'palm.02.L': BoneDefinition(
        head='left_hand_wrist',
        tail='left_hand_middle_finger_mcp',
    ),
    'f_middle.01.R': BoneDefinition(
        head='right_hand_middle_finger_mcp',
        tail='right_hand_middle_finger_pip',
    ),
    'f_middle.01.L': BoneDefinition(
        head='left_hand_middle_finger_mcp',
        tail='left_hand_middle_finger_pip',
    ),
    'f_middle.02.R': BoneDefinition(
        head='right_hand_middle_finger_pip',
        tail='right_hand_middle_finger_dip',
    ),
    'f_middle.02.L': BoneDefinition(
        head='left_hand_middle_finger_pip',
        tail='left_hand_middle_finger_dip',
    ),
    'f_middle.03.R': BoneDefinition(
        head='right_hand_middle_finger_dip',
        tail='right_hand_middle_finger_tip',
    ),
    'f_middle.03.L': BoneDefinition(
        head='left_hand_middle_finger_dip',
        tail='left_hand_middle_finger_tip',
    ),
    'palm.03.R': BoneDefinition(
        head='right_hand_wrist',
        tail='right_hand_ring_finger_mcp',
    ),
    'palm.03.L': BoneDefinition(
        head='left_hand_wrist',
        tail='left_hand_ring_finger_mcp',
    ),
    'f_ring.01.R': BoneDefinition(
        head='right_hand_ring_finger_mcp',
        tail='right_hand_ring_finger_pip',
    ),
    'f_ring.01.L': BoneDefinition(
        head='left_hand_ring_finger_mcp',
        tail='left_hand_ring_finger_pip',
    ),
    'f_ring.02.R': BoneDefinition(
        head='right_hand_ring_finger_pip',
        tail='right_hand_ring_finger_dip',
    ),
    'f_ring.02.L': BoneDefinition(
        head='left_hand_ring_finger_pip',
        tail='left_hand_ring_finger_dip',
    ),
    'f_ring.03.R': BoneDefinition(
        head='right_hand_ring_finger_dip',
        tail='right_hand_ring_finger_tip',
    ),
    'f_ring.03.L': BoneDefinition(
        head='left_hand_ring_finger_dip',
        tail='left_hand_ring_finger_tip',
    ),
    'palm.04.R': BoneDefinition(
        head='right_hand_wrist',
        tail='right_hand_pinky_mcp',
    ),
    'palm.04.L': BoneDefinition(
        head='left_hand_wrist',
        tail='left_hand_pinky_mcp',
    ),
    'f_pinky.01.R': BoneDefinition(
        head='right_hand_pinky_mcp',
        tail='right_hand_pinky_pip',
    ),
    'f_pinky.01.L': BoneDefinition(
        head='left_hand_pinky_mcp',
        tail='left_hand_pinky_pip',
    ),
    'f_pinky.02.R': BoneDefinition(
        head='right_hand_pinky_pip',
        tail='right_hand_pinky_dip',
    ),
    'f_pinky.02.L': BoneDefinition(
        head='left_hand_pinky_pip',
        tail='left_hand_pinky_dip',
    ),
    'f_pinky.03.R': BoneDefinition(
        head='right_hand_pinky_dip',
        tail='right_hand_pinky_tip',
    ),
    'f_pinky.03.L': BoneDefinition(
        head='left_hand_pinky_dip',
        tail='left_hand_pinky_tip',
    ),
    'thigh.R': BoneDefinition(
        head='right_hip',
        tail='right_knee',
    ),
    'thigh.L': BoneDefinition(
        head='left_hip',
        tail='left_knee',
    ),
    'shin.R': BoneDefinition(
        head='right_knee',
        tail='right_ankle',
    ),
    'shin.L': BoneDefinition(
        head='left_knee',
        tail='left_ankle',
    ),
    'foot.R': BoneDefinition(
        head='right_ankle',
        tail='right_foot_index',
    ),
    'foot.L': BoneDefinition(
        head='left_ankle',
        tail='left_foot_index',
    ),
    'heel.02.R': BoneDefinition(
        head='right_ankle',
        tail='right_heel',
    ),
    'heel.02.L': BoneDefinition(
        head='left_ankle',
        tail='left_heel',
    ),
}

def get_bone_definitions():
    """
    Returns a deep copy of the bone definitions, to ensure the base definitions isn't modified.
    """
    return deepcopy(_BONE_DEFINITIONS)