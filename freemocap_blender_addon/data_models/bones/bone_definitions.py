from dataclasses import dataclass
from typing import Dict, Literal, Union, Tuple, List

BoneName = str  # TODO - create a custom type for this with validators for things like the .R and .001 suffixes
HandName = Literal['left_hand', 'right_hand']


@dataclass
class BoneDefinition:
    head: str
    tail: str
    length: float = 0.0  # Assuming default length is 0.0 if not provided

@dataclass
class BodyBoneDefinitions:
    bones: Dict[BoneName, BoneDefinition]

@classmethod
class HandBoneDefinitions:
    right: Dict[BoneName, BoneDefinition]
    left: Dict[BoneName, BoneDefinition]


@dataclass
class SkeletonBoneDefinitions:
    body: BodyBoneDefinitions
    hands: HandBoneDefinitions





AXIAL_BONE_DEFINITIONS = {
    'pelvis': {'head': 'hips_center', 'tail': 'hip'},
    'spine': {'head': 'hips_center', 'tail': 'trunk_center'},
    'spine.001': {'head': 'trunk_center', 'tail': 'neck_center'},
    'neck': {'head': 'neck_center', 'tail': 'head_center'},
    'head_nose': {'head': 'head_center', 'tail': 'nose'}
}

MIRRORED_BODY_BONE_DEFINITIONS = {
    'clavicle': {'head': 'neck_center', 'tail': 'shoulder'},
    'upper_arm': {'head': 'shoulder', 'tail': 'elbow'},
    'forearm': {'head': 'elbow', 'tail': 'wrist'},
    'hand': {'head': 'wrist', 'tail': 'index'},
    'thigh': {'head': 'hip', 'tail': 'knee'},
    'shin': {'head': 'knee', 'tail': 'ankle'},
    'foot': {'head': 'ankle', 'tail': 'foot_index'},
    'heel.02': {'head': 'ankle', 'tail': 'heel'},
}


# Base hand bone definitions without suffixes
BASE_HAND_BONE_DEFINITIONS = {
    'thumb.carpal': {'head': 'hand_wrist', 'tail': 'hand_thumb_cmc'},
    'thumb.01': {'head': 'hand_thumb_cmc', 'tail': 'hand_thumb_mcp'},
    'thumb.02': {'head': 'hand_thumb_mcp', 'tail': 'hand_thumb_ip'},
    'thumb.03': {'head': 'hand_thumb_ip', 'tail': 'hand_thumb_tip'},

    'palm.01': {'head': 'hand_wrist', 'tail': 'hand_index_finger_mcp'},
    'f_index.01': {'head': 'hand_index_finger_mcp', 'tail': 'hand_index_finger_pip'},
    'f_index.02': {'head': 'hand_index_finger_pip', 'tail': 'hand_index_finger_dip'},
    'f_index.03': {'head': 'hand_index_finger_dip', 'tail': 'hand_index_finger_tip'},

    'palm.02': {'head': 'hand_wrist', 'tail': 'hand_middle_finger_mcp'},
    'f_middle.01': {'head': 'hand_middle_finger_mcp', 'tail': 'hand_middle_finger_pip'},
    'f_middle.02': {'head': 'hand_middle_finger_pip', 'tail': 'hand_middle_finger_dip'},
    'f_middle.03': {'head': 'hand_middle_finger_dip', 'tail': 'hand_middle_finger_tip'},

    'palm.03': {'head': 'hand_wrist', 'tail': 'hand_ring_finger_mcp'},
    'f_ring.01': {'head': 'hand_ring_finger_mcp', 'tail': 'hand_ring_finger_pip'},
    'f_ring.02': {'head': 'hand_ring_finger_pip', 'tail': 'hand_ring_finger_dip'},
    'f_ring.03': {'head': 'hand_ring_finger_dip', 'tail': 'hand_ring_finger_tip'},

    'palm.04': {'head': 'hand_wrist', 'tail': 'hand_pinky_mcp'},
    'f_pinky.01': {'head': 'hand_pinky_mcp', 'tail': 'hand_pinky_pip'},
    'f_pinky.02': {'head': 'hand_pinky_pip', 'tail': 'hand_pinky_dip'},
    'f_pinky.03': {'head': 'hand_pinky_dip', 'tail': 'hand_pinky_tip'}
}



