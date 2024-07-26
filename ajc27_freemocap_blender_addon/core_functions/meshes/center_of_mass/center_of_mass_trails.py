# from typing import Tuple
from typing import Tuple

import bpy
import numpy as np
from ajc27_freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import \
    create_keyframed_empty_from_3d_trajectory_data


def create_trail_empties(trajectory: np.ndarray,
                         parent_object: bpy.types.Object,
                         tail_past_frames: int,
                         trail_future_frames: int):
    """
    Create a trail of empties from a center of mass empty that correspond to the center of mass empty's location on past and future frames.    
    """

    past_com_trail_empties = []
    for frame in range(1, tail_past_frames + 1):
        past_shifted_trajectory = np.vstack((trajectory[:frame, :], trajectory[:-frame, :]))
        past_com_trail_empties.append(create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=past_shifted_trajectory,
            trajectory_name=f"past_com_trail_empty_{frame}",
            parent_object=parent_object,
            empty_scale=0.01,
            empty_type="SPHERE",
        )
        )

    future_com_trail_empties = []
    for frame in range(trail_future_frames):
        future_shifted_trajectory = np.vstack((trajectory[frame:, :], trajectory[:frame, :]))
        future_com_trail_empties.append(create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=future_shifted_trajectory,
            trajectory_name=f"future_com_trail_empty_{frame}",
            parent_object=parent_object,
            empty_scale=0.01,
            empty_type="SPHERE",
        )
        )
    return {"past": past_com_trail_empties, "future": future_com_trail_empties}


def create_center_of_mass_trails(center_of_mass_trajectory: np.ndarray,
                                 parent_empty: bpy.types.Object,
                                 tail_past_frames: int,
                                 trail_future_frames: int,
                                 trail_starting_width: float,
                                 trail_minimum_width: float,
                                 trail_size_decay_rate: float,
                                 trail_color: Tuple[float, float, float, float],
                                 ):
    com_trail_empties = create_trail_empties(trajectory=center_of_mass_trajectory,
                                             parent_object=parent_empty,
                                             tail_past_frames=tail_past_frames,
                                             trail_future_frames=trail_future_frames)
    for direction, empties in com_trail_empties.items():
        for empty_number, empty in enumerate(empties):
            scale = trail_starting_width * (trail_size_decay_rate ** empty_number)
            if scale < trail_minimum_width:
                scale = trail_minimum_width

            length = 1  # Default length for now
            if empty_number < len(empties) - 1:
                # Here we calculate the distance to the next empty to set length
                length = (empties[empty_number + 1].location - empty.location).length

            # trail_point_mesh = make_bone_mesh(name=f"com_trail_sphere_{empty_number}",
            #                                   axis_visible=False,
            #                                   length=length,
            #                                   squish_scale=(1, 1, 1),
            #                                   )
            bpy.ops.mesh.primitive_uv_sphere_add(segments=8,
                                                    ring_count=8,
                                                    scale=(scale, scale, scale),
                                                    )                               
            trail_point_mesh = bpy.context.active_object
            trail_point_mesh.name = f"{empty.name}_trail_sphere"
            trail_point_mesh.parent = empty


            if empty_number < len(empties) - 1:
                damped_track_constraint = trail_point_mesh.constraints.new(type='DAMPED_TRACK')
                damped_track_constraint.target = empties[empty_number + 1]
                damped_track_constraint.track_axis = 'TRACK_Z'
                # driver = trail_point_mesh.driver_add("scale", 2).driver
                # driver.type = 'SCRIPTED'
                
                # dist_var = driver.variables.new()
                # dist_var.name = 'dist'
                # dist_var.type = 'LOC_DIFF'
                
                # # Targets
                # dist_var.targets[0].id = empties[empty_number]
                # dist_var.targets[1].id = empties[empty_number + 1]

                # driver.expression = 'dist'

            empty.hide_set(True)
