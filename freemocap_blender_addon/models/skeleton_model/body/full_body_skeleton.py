from freemocap_blender_addon.models.skeleton_model.body.chains.axial_body_chain import AxialBodyChain
from freemocap_blender_addon.models.skeleton_model.body.chains.left_body_chains import LeftArmChain, LeftLegChain
from freemocap_blender_addon.models.skeleton_model.body.chains.right_body_chains import RightArmChain, RightLegChain
from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import SkeletonABC


class FullBodySkeleton(SkeletonABC):
    parent = AxialBodyChain
    children = [RightArmChain,
                RightLegChain,
                LeftArmChain,
                LeftLegChain]



if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_rest_recording

    recording_data = load_freemocap_rest_recording()
    keypoint_trajectories = recording_data.body.map_to_keypoints()
    skeleton = FullBodySkeleton.from_keypoint_trajectories(keypoint_trajectories)
