from typing import Dict

from skelly_blender.core.pure_python.custom_types.generic_types import TrackedPointName, SegmentName, KeypointName
from skelly_blender.core.pure_python.rigid_bodies.rigid_body_definition_class import RigidBodyDefinition
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.pure_python.utility_classes.sample_statistics import DescriptiveStatistics

Trajectories = Dict[str, Trajectory] #TODO - Make an AllKeypointsEnum or something
KeypointTrajectories = Dict[str, Trajectory] #TODO - ditto above
SegmentStats = Dict[SegmentName, DescriptiveStatistics]
RigidBodyDefinitions = Dict[SegmentName, RigidBodyDefinition]
