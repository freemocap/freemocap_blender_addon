from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import combine_enums, LeftLegKeypoints, \
    LeftMittenHandKeypoints, LeftArmKeypoints, RightLegKeypoints, RightMittenHandKeypoints, RightArmKeypoints, \
    AxialSkeletonKeypoints
from freemocap_blender_addon.models.skeleton_model.body.rigid_bodies.skull_rigid_bodies import SkullRigidBodies


BodyRigidBodies = Enum('BodyRigidBodies', combine_enums(
    SkullRigidBodies,
    AxialSkeletonKeypoints,
    RightArmKeypoints,
    RightMittenHandKeypoints,
    RightLegKeypoints,
    LeftArmKeypoints,
    LeftMittenHandKeypoints,
    LeftLegKeypoints,

))

# Example usage
if __name__ == "__main__":
    print("\n".join([f"{kp.name}: {kp.value}" for kp in list(BodyRigidBodies)]))
