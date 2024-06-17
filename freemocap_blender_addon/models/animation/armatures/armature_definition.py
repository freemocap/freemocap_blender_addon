from collections import defaultdict, deque
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, Tuple, List

from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import BonePoseDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose.pose_types import PoseTypes
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name, BlenderizedName
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ArmatureBoneDefinition:
    rest_pose: BonePoseDefinition
    length: float

    @property
    def is_root(self):
        return self.rest_pose.parent_bone_name == "ROOT"

    @property
    def parent(self):
        return self.rest_pose.parent_bone_name


ROOT_ARMATURE_BONE_DEFINTIION = ArmatureBoneDefinition(
    rest_pose=BonePoseDefinition(
        rotation=(0, 0, 0),
        is_connected=False,
        parent_bone_name=None,
    ),
    length=0.1,
)


@dataclass
class ArmatureDefinition(TypeSafeDataclass):
    armature_name: str
    bone_definitions: Dict[BlenderizedName, ArmatureBoneDefinition]

    @classmethod
    def create(cls,
               rig_name: str,
               segment_definitions: RigidSegmentDefinitions,
               pose_definition: PoseTypes):
        bone_definitions = {"ROOT": ROOT_ARMATURE_BONE_DEFINTIION}
        for segment_name, segment in segment_definitions.items():
            bone_definitions[blenderize_name(segment_name)] = ArmatureBoneDefinition(
                rest_pose=pose_definition.value[blenderize_name(segment_name)].value,
                length=segment.length,
            )

        return cls(
            armature_name=rig_name,
            bone_definitions=bone_definitions,
        )

    def build_dependency_graph(self) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
        dependency_graph = defaultdict(list)
        indegree = defaultdict(int)  # the number of incoming edges to a node

        for bone_name, bone_def in self.bone_definitions.items():
            parent_name = bone_def.parent
            if parent_name == "ROOT":
                indegree[bone_name] = 0
            else:
                dependency_graph[parent_name].append(bone_name)
                indegree[parent_name] += 1

        print("Dependency Graph:")
        pprint(dict(dependency_graph), indent=4)
        print("Initial Indegree:")
        pprint(dict(indegree), indent=4)
        return dependency_graph, indegree

    def topological_sort(self) -> List[str]:
        dependency_graph, indegree = self.build_dependency_graph()
        sorted_bones = []
        queue = deque([bone for bone in indegree if indegree[bone] == 0])

        while queue:
            parent = queue.popleft()
            sorted_bones.append(parent)
            for child in dependency_graph[parent]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

        # Check if there's any node left unprocessed (cycle detection)
        if len(sorted_bones) != len(self.bone_definitions):
            raise ValueError("The dependency graph has cycles or disconnected components.")

        print("Sorted Bones:")
        pprint(sorted_bones, indent=4)
        return sorted_bones

    def get_sorted_bone_list(self) -> List[str]:
        return self.topological_sort()


if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_test_recording
    from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
        calculate_rigid_body_trajectories
    from freemocap_blender_addon.models.skeleton_model import SkeletonTypes

    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer, segment_definitions_outer = calculate_rigid_body_trajectories(
        keypoint_trajectories=recording_data.body.map_to_keypoints(),
        skeleton_definition=SkeletonTypes.BODY_ONLY)

    armature_definition=ArmatureDefinition.create(
        rig_name="rig",
        segment_definitions=segment_definitions_outer,
        pose_definition=PoseTypes.DEFAULT_TPOSE,
    )
    armature_definition.get_sorted_bone_list()
