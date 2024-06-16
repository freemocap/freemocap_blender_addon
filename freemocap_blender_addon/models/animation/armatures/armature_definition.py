from dataclasses import dataclass
from typing import List, Dict

from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.armature_bone_info import ArmatureBoneDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose import PoseTypes
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.linkage_abc import LinkageABC
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name, BlenderizedName
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ArmatureDefinition(TypeSafeDataclass):
    rig_name: str
    bone_definitions: Dict[BlenderizedName, ArmatureBoneDefinition]
    add_ik_constraints: bool

    def __post_init__(self):
        for linkage in self.linkages:
            if not linkage.parent.name in self.segment_definitions.keys():
                raise ValueError(f"Linkage parent {linkage.parent.name} not found in segment definitions")
            for child in linkage.children:
                if not child.name in self.segment_definitions.keys():
                    raise ValueError(f"Linkage child {child.name} not found in segment definitions")


    @classmethod
    def create_from_segment_definitions(cls,
                                        rig_name: str,
                                        segment_definitions: RigidSegmentDefinitions,
                                        linkages: List[LinkageABC],
                                        pose_definition: PoseTypes,
                                        add_ik_constraints: bool):
        armature_bone_names = [blenderize_name(segment_name) for segment_name in segment_definitions.keys()]
