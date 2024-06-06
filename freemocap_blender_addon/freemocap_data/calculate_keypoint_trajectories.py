import numpy as np

from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import SkeletonMappingEnum, \
    KeypointMappingType

# names, trajectory_data = calculate_keypoint_trajectories(data=data,
#                                                          names=get_keypoint_names(
#                                                              component_type=ComponentType.BODY,
#                                                              data_source=data_source),
#                                                          keypoint_mapping=get_mapping(
#                                                              component_type=ComponentType.BODY,
#                                                              data_source=data_source),
#                                                          )


def calculate_keypoint_trajectories(data: np.ndarray,
                                    names: list,
                                    keypoint_mapping: SkeletonMappingEnum) -> np.ndarray:
    """
    Create a virtual marker from a set of component markers. A 'Virtual Marker' is a 'fake' marker created by combining the data from 'real' (measured) marker/trajectory data.
    """
    number_of_frames = data.shape[0]
    number_of_dimensions = data.shape[2]
    trajectories_frame_xyz = np.zeros((number_of_frames, number_of_dimensions), dtype=np.float32)

    for keypoint_name, mapping in keypoint_mapping.__class__:
        # pull out the trajectory data for this component trajectory and scale by its weight
        trajectory_xyz = calculate_trajectory_from_mapping(data=data,
                                                           mapping=mapping,
                                                           names=names)
        trajectories_frame_xyz += component_xyz

    if trajectories_frame_xyz.shape[0] != data.shape[0] or trajectories_frame_xyz.shape[1] != data.shape[2]:
        raise ValueError(
            f"Virtual marker {definition.name} has shape {trajectories_frame_xyz.shape} but should have shape ({data.shape[0]},"
            f" {data.shape[2]})"
        )

    return trajectories_frame_xyz


def calculate_trajectory_from_mapping(data: np.ndarray,
                                      mapping: KeypointMappingType,
                                      names: list) -> np.ndarray:
    """
    Calculate a trajectory from a mapping of tracked points and their weights.
    """
    number_of_frames = data.shape[0]
    number_of_dimensions = data.shape[2]
    trajectories_frame_xyz = np.zeros((number_of_frames, number_of_dimensions), dtype=np.float32)

    for keypoint_name, weight in definition.items():
        if keypoint_name not in names:
            raise ValueError(f"Key {keypoint_name} not found in trajectory names")

    return trajectories_frame_xyz
