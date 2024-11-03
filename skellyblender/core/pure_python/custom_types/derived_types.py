from typing import Dict

from skellyblender.core.pure_python.custom_types.generic_types import SegmentName
from skellyblender.core.pure_python.rigid_bodies.rigid_body_definition_class import RigidBodyDefinition
from skellyblender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory
from skellyblender.core.pure_python.math_stuff.sample_statistics import DescriptiveStatistics

Trajectories = Dict[str, Trajectory] #TODO - Make an AllKeypointsEnum or something
KeypointTrajectories = Dict[str, Trajectory] #TODO - ditto above
SegmentStats = Dict[SegmentName, DescriptiveStatistics]
RigidBodyDefinitions = Dict[SegmentName, RigidBodyDefinition]
