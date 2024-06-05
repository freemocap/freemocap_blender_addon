from typing import List, Tuple

import numpy as np

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import WeightedSumDefiniton


def calculate_virtual_trajectory(data: np.ndarray,
                                 names: list,
                                 definition: WeightedSumDefiniton) -> np.ndarray:
    """
    Create a virtual marker from a set of component markers. A 'Virtual Marker' is a 'fake' marker created by combining the data from 'real' (measured) marker/trajectory data.
    """
    if definition.name in names:
        raise ValueError(f"Virtual marker name {definition.name} already exists in trajectory names list")
    number_of_frames = data.shape[0]
    number_of_dimensions = data.shape[2]
    virtual_trajectory_frame_xyz = np.zeros((number_of_frames, number_of_dimensions), dtype=np.float32)

    for name, weight in zip(definition.parent_keypoints, definition.weights):
        # pull out the trajectory data for this component trajectory and scale by its weight
        component_xyz = data[:, names.index(name), :] * weight
        virtual_trajectory_frame_xyz += component_xyz

    if virtual_trajectory_frame_xyz.shape[0] != data.shape[0] or virtual_trajectory_frame_xyz.shape[1] != data.shape[2]:
        raise ValueError(
            f"Virtual marker {definition.name} has shape {virtual_trajectory_frame_xyz.shape} but should have shape ({data.shape[0]},"
            f" {data.shape[2]})"
        )

    return virtual_trajectory_frame_xyz


def add_virtual_trajectories(data: np.ndarray,
                             names: List[str],
                             virtual_trajectory_definitions: List[WeightedSumDefiniton]) -> Tuple[
    List[str], np.ndarray]:
    """
    Create virtual markers from the body data using the marker definitions.
    """
    print("Creating virtual markers...")

    for virtual_trajectory_definition in virtual_trajectory_definitions:
        print(f"Calculating virtual marker trajectory: {virtual_trajectory_definition.name} \n"
              f"Component trajectories: {virtual_trajectory_definition.parent_keypoints} \n"
              f" weights: {virtual_trajectory_definition.weights}\n")

        virtual_trajectory_frame_xyz = calculate_virtual_trajectory(
            data=data,
            names=names,
            definition=virtual_trajectory_definition
        )

        names.append(virtual_trajectory_definition.name)
        data = np.concatenate((data, virtual_trajectory_frame_xyz[:, np.newaxis, :]), axis=1)

    if len(names) != data.shape[1]:
        raise ValueError(f"Number of names {len(names)} does not match number of trajectories {data.shape[1]}")
    return names, data
