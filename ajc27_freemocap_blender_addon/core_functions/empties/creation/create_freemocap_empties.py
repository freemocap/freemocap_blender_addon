import bpy
from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler

from .create_empty_from_trajectory import create_empties

BODY_EMPTY_SCALE = 0.03


def create_freemocap_empties(handler: FreemocapDataHandler,
                             parent_object: bpy.types.Object,
                             center_of_mass_data_parent: bpy.types.Object,
                             body_empty_scale: float = BODY_EMPTY_SCALE,
                             ):
    hand_empty_scale = body_empty_scale * 0.5
    print("Loading freemocap trajectory data as keyframed empties....")

    empties = {}
    try:
        # body trajectories
        empties["body"] = create_empties(trajectory_frame_marker_xyz=handler.body_frame_name_xyz,
                                         names_list=handler.body_names,
                                         empty_scale=body_empty_scale,
                                         empty_type="SPHERE",
                                         parent_object=parent_object, )

        empties["hands"] = {}
        # right hand trajectories
        empties["hands"]["right"] = create_empties(
            trajectory_frame_marker_xyz=handler.right_hand_frame_name_xyz,
            names_list=handler.right_hand_names,
            empty_scale=hand_empty_scale,
            empty_type="PLAIN_AXES",
            parent_object=parent_object,
        )
        # left hand trajectories
        empties["hands"]["left"] = create_empties(
            trajectory_frame_marker_xyz=handler.left_hand_frame_name_xyz,
            names_list=handler.left_hand_names,
            empty_scale=hand_empty_scale,
            empty_type="PLAIN_AXES",
            parent_object=parent_object,
        )

        empties["other"] = {}
        empties["other"]["center_of_mass"] = create_empties(
            trajectory_frame_marker_xyz=handler.center_of_mass_trajectory,
            names_list="center_of_mass",
            empty_scale=body_empty_scale * 3,
            empty_type="ARROWS",
            parent_object=center_of_mass_data_parent
        )
        return empties

    except Exception as e:
        print(f"Failed to load freemocap trajectory data as keyframed empties: {e}")
        print(f"{e}")

        raise e
