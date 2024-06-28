from typing import Tuple, List, Union

import bpy
import numpy as np
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy


def translate_empty_and_its_children(empty_name: str,
                                     frame_index: int,
                                     delta: Union[List[float], Tuple[float, float, float], np.ndarray]):
    mediapipe_hierarchy = get_mediapipe_hierarchy()
    if isinstance(delta, np.ndarray) or isinstance(delta, tuple):
        delta = list(delta)

    if not len(delta) == 3:
        raise ValueError(f"Delta must be a list of length 3, not {len(delta)}")

    try:
        # Translate the empty in the animation location curve

        bpy.data.objects[empty_name].animation_data.action.fcurves[0].keyframe_points[frame_index].co[1] += delta[0]

        bpy.data.objects[empty_name].animation_data.action.fcurves[1].keyframe_points[frame_index].co[1] += delta[1]

        bpy.data.objects[empty_name].animation_data.action.fcurves[2].keyframe_points[frame_index].co[1] = delta[2]
    except:
        # Empty does not exist or does not have animation data
        # print('Empty ' + empty + ' does not have animation data on frame ' + str(frame_index))
        pass

    # If empty has children then call this function for every child
    if empty_name in mediapipe_hierarchy.keys():
        print(
            f"Translating children of empty {empty_name}: {mediapipe_hierarchy[empty_name]['children']}")
        for child in mediapipe_hierarchy[empty_name]['children']:
            translate_empty_and_its_children(empty_name=child,
                                             frame_index=frame_index,
                                             delta=delta)
