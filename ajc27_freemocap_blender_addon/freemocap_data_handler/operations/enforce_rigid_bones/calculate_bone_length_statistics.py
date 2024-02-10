import math
import statistics
from typing import Dict, Any
from ajc27_freemocap_blender_addon.system.configure_logging.configure_logging import LogStrings

import numpy as np


def calculate_bone_length_statistics(trajectories: Dict[str, np.ndarray],
                                     bones: Dict[str, Dict[str, Any]]):
    print(LogStrings.INFO, 'Calculating bone length statistics...')

    # Reset the lengths list for every virtual bone
    for bone in bones:
        bones[bone]['lengths'] = []

    bones['hand.R']['tail'] = 'right_hand_middle'
    bones['hand.L']['tail'] = 'left_hand_middle'

    # Iterate through the empty_positions dictionary and calculate the distance between the head and tail and append it to the lengths list
    for frame_number in range(0, trajectories['hips_center'].shape[0]):
        # Iterate through each bone
        for bone_name, bone_dict in bones.items():
            # Calculate the length of the bone for this frame
            head_name = bone_dict['head']
            tail_name = bone_dict['tail']

            head_pos = list(trajectories[head_name][frame_number, :])
            tail_pos = list(trajectories[tail_name][frame_number, :])

            bone_dict['lengths'].append(math.dist(head_pos, tail_pos))

    print(f'{LogStrings.INFO} Bone lengths calculated successfully!')
    # Update the length median and stdev values for each bone
    for name, bone in bones.items():
        print(f'{LogStrings.DEBUG} Calculating median and stdev for bone: {name}...')
        # Exclude posible length NaN (produced by an empty with NaN values as position) values from the median and standard deviation
        bone['median'] = statistics.median(
            [length for length in bone['lengths'] if not math.isnan(length)])
        # virtual_bone['median'] = statistics.median(virtual_bone['lengths'])
        bone['stdev'] = statistics.stdev(
            [length for length in bone['lengths'] if not math.isnan(length)])
        # virtual_bone['stdev'] = statistics.stdev(virtual_bone['lengths'])

    print(f'{LogStrings.INFO} Bone length statistics calculated successfully!')

    return bones
