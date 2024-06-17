import bpy
from dataclasses import dataclass
from typing import Tuple, Optional, List, Dict
from mathutils import Euler, Vector
from collections import defaultdict, deque
from pprint import pprint


@dataclass
class Bone:
    name: str
    length: float
    rotation: Tuple[float, float, float]  # Rotation in parent local coordinates (Euler angles)
    parent: Optional[str]  # Name of the parent bone, or None if root
    connect_to: str  # "HEAD" or "TAIL"
    connect: bool  # Whether to connect to the parent
    offset: Tuple[float, float, float]  # XYZ offset from the parent


def build_dependency_graph(bones: List[Bone]) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    dependency_graph = defaultdict(list)
    indegree = defaultdict(int)

    for bone in bones:
        if bone.parent:
            dependency_graph[bone.parent].append(bone.name)
            indegree[bone.name] += 1
        else:
            indegree[bone.name] = 0

    return dependency_graph, indegree


def topological_sort(dependency_graph: Dict[str, List[str]], indegree: Dict[str, int]) -> List[str]:
    sorted_bones = []
    queue = deque([bone for bone in indegree if indegree[bone] == 0])

    while queue:
        parent = queue.popleft()
        sorted_bones.append(parent)
        for child in dependency_graph[parent]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    return sorted_bones


def get_bone_position(armature, parent_name: Optional[str], connect_to: str,
                      offset: Tuple[float, float, float]) -> Vector:
    if parent_name is None:
        return Vector((0, 0, 0))

    parent_bone = armature.edit_bones[parent_name]
    if connect_to == 'HEAD':
        parent_position = parent_bone.head
    else:
        parent_position = parent_bone.tail

    return parent_position + Vector(offset)


def create_armature(bones: List[Bone], sorted_bones: List[str]):
    armature = bpy.data.armatures.new('MyComplexArmature')
    armature_obj = bpy.data.objects.new('MyComplexArmatureObject', armature)

    # Link the object to the scene collection
    bpy.context.collection.objects.link(armature_obj)

    # Enter edit mode
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Create a dictionary for quick lookup of bone data by name
    bone_data_dict = {bone.name: bone for bone in bones}

    # Add the ROOT bone
    root_bone = armature.edit_bones.new('ROOT')
    root_bone.head = Vector((0, 0, 0))
    root_bone.tail = Vector((-0.1, 0, 0))

    # Create bones in sorted order
    for bone_name in sorted_bones:
        if bone_name == 'ROOT':
            continue

        bone_data = bone_data_dict[bone_name]

        # Create the new bone
        bone = armature.edit_bones.new(bone_data.name)

        # Set the head position
        bone.head = get_bone_position(armature, bone_data.parent, bone_data.connect_to, bone_data.offset)

        # Calculate the tail position based on length and rotation
        local_tail = Vector((0, 0, bone_data.length))
        rotation_matrix = Euler(bone_data.rotation, 'XYZ').to_matrix().to_3x3()
        rotated_tail = bone.head + rotation_matrix @ local_tail
        bone.tail = rotated_tail

        # Set the parent bone and connection
        if bone_data.parent:
            bone.parent = armature.edit_bones[bone_data.parent]
            bone.use_connect = bone_data.connect

        # Debugging prints
        print(
            f"Created bone '{bone_data.name}' with head at {bone.head} and tail at {bone.tail}, parent: {bone_data.parent}")

    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    print(f"Armature '{armature_obj.name}' created with bones: {[bone.name for bone in bones]}")


def main():
    # List of bones
    bones = [
        Bone(name='Bone1', length=2.0, rotation=(0, 0, 0), parent='ROOT', connect_to='TAIL', connect=False,
             offset=(0, 0, 0)),
        Bone(name='Bone2', length=1.5, rotation=(0.5, 0, 0), parent='Bone1', connect_to='TAIL', connect=True,
             offset=(0, 0, 0)),
        Bone(name='Bone3', length=1.0, rotation=(0, 0.5, 0), parent='Bone1', connect_to='TAIL', connect=False,
             offset=(0, 0, 0)),
        Bone(name='Bone4', length=1.5, rotation=(0, 0, 0.5), parent='Bone2', connect_to='TAIL', connect=True,
             offset=(0, 0, 0)),
        Bone(name='Bone5', length=0.8, rotation=(0, 0, 0), parent='Bone2', connect_to='TAIL', connect=False,
             offset=(0, 0, 0)),
    ]

    dependency_graph, indegree = build_dependency_graph(bones)
    sorted_bones = topological_sort(dependency_graph, indegree)
    # Debugging the dependency graph and sorted bones
    print("Dependency Graph:")
    pprint(dict(dependency_graph), indent=4)

    print("Initial Indegree:")
    pprint(dict(indegree), indent=4)



    print("Sorted Bones:")
    pprint(sorted_bones, indent=4)

    create_armature(bones, sorted_bones)


if __name__ == "__main__":
    main()