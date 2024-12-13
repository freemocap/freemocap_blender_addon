import math
import statistics
from typing import Dict, Any

import numpy as np

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import BoneDefinition


def calculate_bone_length_statistics(trajectories: Dict[str, np.ndarray],
                                     bone_definitions: Dict[str, BoneDefinition]):
    print('Calculating bone length statistics...')

    # Reset the lengths list for every virtual bone
    for bone in bone_definitions:
        bone_definitions[bone].lengths = []

    bone_definitions['hand.R'].tail = 'right_hand_middle'
    bone_definitions['hand.L'].tail = 'left_hand_middle'

    # Iterate through the empty_positions dictionary and calculate the distance between the head and tail and append it to the lengths list
    for frame_number in range(0, trajectories['hips_center'].shape[0]):
        # Iterate through each bone
        for bone_name, bone_definition in bone_definitions.items():
            # Calculate the length of the bone for this frame
            head_name = bone_definition.head
            tail_name = bone_definition.tail

            head_pos = list(trajectories[head_name][frame_number, :])
            tail_pos = list(trajectories[tail_name][frame_number, :])

            bone_definition.lengths.append(math.dist(head_pos, tail_pos))

    print(f'Bone lengths calculated successfully!\n bones: \n{list(bone_definitions.keys())}')
    # Update the length median and stdev values for each bone
    for name, bone in bone_definitions.items():
        # print(f'Calculating median and stdev for bone: {name}...')
        # Exclude posible length NaN (produced by an empty with NaN values as position) values from the median and standard deviation
        bone.median = statistics.median(
            [length for length in bone.lengths if not math.isnan(length)])
        # virtual_bone['median'] = statistics.median(virtual_bone['lengths'])
        bone.stdev = statistics.stdev(
            [length for length in bone.lengths if not math.isnan(length)])
        # virtual_bone['stdev'] = statistics.stdev(virtual_bone['lengths'])

    print(f'Bone length statistics calculated successfully!')

    return bone_definitions
