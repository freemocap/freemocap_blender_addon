import math

import bpy
import bmesh
from mathutils import Matrix


def _is_invalid_vector(vector) -> bool:
    return vector.length == 0 or any(math.isnan(c) for c in vector)


def rotate_vertex_groups(target_mesh, vertex_groups, bone_info):
    for vertex_group, info in vertex_groups.items():

        # Get the vertex group index
        vertex_group_index = target_mesh.vertex_groups[vertex_group].index

        # Get the origin vertex group index
        origin_vertex_group_index = target_mesh.vertex_groups[vertex_group + '_origin'].index

        # Try to get the end vertex group index
        try:
            end_vertex_group_index = target_mesh.vertex_groups[vertex_group + '_end'].index
        except KeyError:
            print(f"The vertex group '{vertex_group}_end' does not exist.")
            end_vertex_group_index = None

        # Find the origin and end vertices
        origin_vertex = None
        end_vertex = None
        for vert in target_mesh.data.vertices:
            for group in vert.groups:
                if group.group == origin_vertex_group_index:
                    origin_vertex = vert
                    break
                if group.group == end_vertex_group_index:
                    end_vertex = vert
                    break
            if origin_vertex and end_vertex:
                break

        if origin_vertex is not None and end_vertex is not None:
            if info['armature_bone'] not in bone_info:
                print(f"Skipping rotation for vertex group '{vertex_group}': "
                      f"bone '{info['armature_bone']}' not found on rig — leaving unrotated.")
                continue

            # Calculate the vertex group vector
            vertex_group_vector = end_vertex.co - origin_vertex.co

            # Get the bone vector
            bone_vector = bone_info[info['armature_bone']]['tail_position'] - bone_info[info['armature_bone']]['head_position']

            if _is_invalid_vector(bone_vector) or _is_invalid_vector(vertex_group_vector):
                print(f"Skipping rotation for vertex group '{vertex_group}': "
                      f"invalid bone vector (zero-length or NaN) for '{info['armature_bone']}' — leaving unrotated.")
                continue

            # Normalize the vectors
            vertex_group_vector.normalize()
            bone_vector.normalize()

            # Calculate the rotation axis (cross product of the vectors)
            rotation_axis = vertex_group_vector.cross(bone_vector)

            # Calculate the rotation angle (angle between the vectors)
            rotation_angle = vertex_group_vector.angle(bone_vector)

            # Create the rotation matrix
            rotation_matrix = Matrix.Rotation(rotation_angle, 4, rotation_axis)

            # Get the bmesh representation
            bm = bmesh.from_edit_mesh(target_mesh.data)

            # Ensure we start with no selections
            bpy.ops.mesh.select_all(action='DESELECT')

            # Find and select vertices in the specified vertex group
            for vert in bm.verts:
                bpy_vert = target_mesh.data.vertices[vert.index]
                for group in bpy_vert.groups:
                    if group.group in [vertex_group_index, origin_vertex_group_index, end_vertex_group_index]:
                        vert.select = True
                        break

            # Apply the rotation to the selected vertices
            bmesh.ops.rotate(
                bm,
                cent=bone_info[info['armature_bone']]['head_position'],
                matrix=rotation_matrix,
                verts=[vert for vert in bm.verts if vert.select],
            )

            # Deselect all vertices
            for vert in bm.verts:
                vert.select = False

    return
