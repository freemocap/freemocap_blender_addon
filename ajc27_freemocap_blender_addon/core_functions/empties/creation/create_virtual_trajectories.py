from typing import List, Dict

import numpy as np

from ajc27_freemocap_blender_addon.data_models.mediapipe_names.virtual_trajectories import \
    get_media_pipe_virtual_trajectory_definition


def validate_marker_definitions(virtual_marker_definitions: dict):
    """
    Validate the virtual marker definitions dictionary to ensure that there are the same number of marker names and weights, and that the weights sum to 1
    """
    for virtual_marker_name, virtual_marker_definition in virtual_marker_definitions.items():
        names = virtual_marker_definition["marker_names"]
        weights = virtual_marker_definition["marker_weights"]
        if len(names) != len(weights):
            raise ValueError(
                f"marker_names and marker_weights must be the same length for virtual marker {virtual_marker_name}")
        if sum(weights) != 1:
            raise ValueError(f"marker_weights must sum to 1 for virtual marker {virtual_marker_name}")


def calculate_virtual_trajectory(all_trajectories: np.ndarray,
                                 all_names: list,
                                 component_names: List,
                                 weights: List) -> np.ndarray:
    """
    Create a virtual marker from a set of component markers. A 'Virtual Marker' is a 'fake' marker created by combining the data from 'real' (measured) marker/trajectory data.
    """
    try:
        number_of_frames = all_trajectories.shape[0]
        number_of_dimensions = all_trajectories.shape[2]
        virtual_trajectory_frame_xyz = np.zeros((number_of_frames, number_of_dimensions), dtype=np.float32)

        for name, weight in zip(component_names, weights):
            if name not in all_names:
                raise ValueError(f"Trajectory {name} not found in trajectory names list")

            # pull out the trajectory data for this component trajectory and scale by its weight
            component_xyz = all_trajectories[:, all_names.index(name), :] * weight
            virtual_trajectory_frame_xyz += component_xyz
    except Exception as e:
        print(f"Error calculating virtual marker trajectory: {e}")
        print(e)
        raise
    return virtual_trajectory_frame_xyz


def calculate_virtual_trajectories(body_frame_name_xyz: np.ndarray,
                                   body_names: List[str]) -> Dict[str, np.ndarray]:
    """
    Create virtual markers from the body data using the marker definitions.
    """
    mediapipe_virtual_trajectory_definitions = get_media_pipe_virtual_trajectory_definition()
    print("Creating virtual markers...")
    validate_marker_definitions(mediapipe_virtual_trajectory_definitions)

    virtual_trajectories = {}
    for virtual_trajectory_name, virtual_trajectory_definition in mediapipe_virtual_trajectory_definitions.items():
        # print(f"Calculating virtual marker trajectory: {virtual_trajectory_name} \n"
        #             f"Component trajectories: {virtual_trajectory_definition['marker_names']} \n"
        #             f"weights: {virtual_trajectory_definition['marker_weights']}")

        virtual_trajectory_frame_xyz = calculate_virtual_trajectory(
            all_trajectories=body_frame_name_xyz,
            all_names=body_names,
            component_names=virtual_trajectory_definition["marker_names"],
            weights=virtual_trajectory_definition["marker_weights"]
        )

        if virtual_trajectory_name in body_names:
            raise ValueError(
                f"Virtual marker name {virtual_trajectory_name} is already in the trajectory names list. This will cause problems later. Please choose a different name for your virtual marker.")

        if virtual_trajectory_frame_xyz.shape[0] != body_frame_name_xyz.shape[0] or virtual_trajectory_frame_xyz.shape[
            1] != body_frame_name_xyz.shape[2]:
            raise ValueError(
                f"Virtual marker {virtual_trajectory_name} has shape {virtual_trajectory_frame_xyz.shape} but should have shape ({body_frame_name_xyz.shape[0]}, {body_frame_name_xyz.shape[2]})"
            )
        virtual_trajectories[virtual_trajectory_name] = virtual_trajectory_frame_xyz

        # print(f"Finished calculating virtual marker trajectory: {virtual_trajectories.keys()}")
    return virtual_trajectories
