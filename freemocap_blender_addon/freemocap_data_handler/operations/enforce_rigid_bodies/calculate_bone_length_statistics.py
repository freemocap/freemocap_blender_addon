from typing import Dict

import numpy as np

from freemocap_blender_addon.data_models.bones.bone_definition_models import BoneDefinition, BoneStatistics


def calculate_bone_length_statistics(trajectories: Dict[str, np.ndarray],
                                     bone_definitions: Dict[str, BoneDefinition]) -> Dict[str, BoneStatistics]:
    print('Calculating bone length statistics...')
    bone_stats: Dict[str, BoneStatistics] = {}

    for bone_name, bone_definition in bone_definitions.items():
        bone_stats[bone_name] = BoneStatistics(name=bone_name, definition=bone_definition)

        head_name = bone_definition.head
        tail_name = bone_definition.tail

        head_positions = trajectories[head_name]
        tail_positions = trajectories[tail_name]

        # Calculate the Euclidean distance between head and tail positions for all frames
        distances = np.linalg.norm(head_positions - tail_positions, axis=1)
        bone_definition.lengths = distances.tolist()


    return bone_stats