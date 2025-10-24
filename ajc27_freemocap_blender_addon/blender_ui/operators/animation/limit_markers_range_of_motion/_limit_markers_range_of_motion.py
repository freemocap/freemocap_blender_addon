import bpy
import numpy as np
import math as m
from mathutils import Vector, Matrix
from copy import deepcopy
from dataclasses import make_dataclass, field
import re

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import _BONE_DEFINITIONS
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy


class FREEMOCAP_OT_limit_markers_range_of_motion(bpy.types.Operator):
    bl_idname = 'freemocap._limit_markers_range_of_motion'
    bl_label = 'Limit Markers Range of Motion'
    bl_description = "Limit Markers Range of Motion"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Limiting Markers Range of Motion.......")

        MEDIAPIPE_HIERARCHY = get_mediapipe_hierarchy()

        scene = context.scene
        props = context.scene.freemocap_ui_properties.limit_markers_range_of_motion_properties

        target_categories = []

        if props.limit_palm_markers:
            target_categories.append('palm')
        if props.limit_proximal_phalanx_markers:
            target_categories.append('proximal_phalanx')
        if props.limit_intermediate_phalanx_markers:
            target_categories.append('intermediate_phalanx')
        if props.limit_distal_phalanx_markers:
            target_categories.append('distal_phalanx')
            
        if len(target_categories) == 0:
            print("No target categories selected")
            return {'FINISHED'}
        
        range_of_motion_scale = props.range_of_motion_scale
        hand_locked_track_marker_name = props.hand_locked_track_marker
        hand_damped_track_marker_name = props.hand_damped_track_marker

        BONE_DEFINITIONS = deepcopy(_BONE_DEFINITIONS)
        
        # Create a mutable dataclass for the virtual bones
        VirtualBoneDefinition = make_dataclass(
            'VirtualBoneDefinition',
            fields=[
                *_BONE_DEFINITIONS['pelvis.R'].__dataclass_fields__.keys(),
                ('bone_x_axis', tuple, field(default=(0,0,0))),
                ('bone_y_axis', tuple, field(default=(0,0,0))),
                ('bone_z_axis', tuple, field(default=(0,0,0))),
            ],
            frozen=False
        )

        VirtualBones = {k: VirtualBoneDefinition(**v.__dict__) for k, v in _BONE_DEFINITIONS.items()}

        data_parent_empty = bpy.data.objects[scene.freemocap_properties.scope_data_parent]

        # Select the data_parent_empty
        try:
            data_parent_empty.select_set(True)
            bpy.context.view_layer.objects.active = data_parent_empty
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # TODO: Move this code a separate module as it is used in more than one operator
        # Create a dictionary with all the markers that are children of the data parent empty
        markers = {}
        for child in data_parent_empty.children_recursive:
            if child.type == 'EMPTY' and 'empties_parent' in child.name:
                for marker in child.children:
                    if marker.type == 'EMPTY':
                        # Get the position fcurves
                        fcurve_x = marker.animation_data.action.fcurves.find("location", index=0)
                        fcurve_y = marker.animation_data.action.fcurves.find("location", index=1)
                        fcurve_z = marker.animation_data.action.fcurves.find("location", index=2)

                        # Get the fcurve data as numpy arrays
                        fcurve_data = np.array([
                            [kp.co[1] for kp in fcurve_x.keyframe_points],
                            [kp.co[1] for kp in fcurve_y.keyframe_points],
                            [kp.co[1] for kp in fcurve_z.keyframe_points]
                        ])
                
                        # Save the marker object and its position fcurves in the dictionary
                        markers[marker.name] = {
                            'object': marker,
                            'fcurves': fcurve_data,
                        }

        # Modify the head and tail markers of each virtual bone to match
        # the markers that are children of the data parent empty
        for bone in VirtualBones.values():
            # Set bone.head as the best match of bone.head in markers.keys()
            bone.head = next((k for k in markers.keys() if k.startswith(bone.head)), None)
            # Set bone.tail as the best match of bone.tail in markers.keys()
            bone.tail = next((k for k in markers.keys() if k.startswith(bone.tail)), None)

        # Change the hand bone tail marker with the one in hand_damped_track_marker
        # Consider the current markers in the markers dictionary (strip possible .000 number at the end to compare)
        for side in ['left', 'right']:
            side_initial = side[0].upper()
            target_marker = f"{side}_{hand_damped_track_marker_name}"
            VirtualBones[f'hand.{side_initial}'].tail = next(
                (k for k in markers.keys() if re.sub(r'\.\d{3}$', '', k) == target_marker),
                None
            )

        # Modify the keys and the children values in MEDIAPIPE_HIERARCHY
        # so they match the markers that are children of the data parent empty
        for marker in markers.keys():
            # Get the closest match of marker in MEDIAPIPE_HIERARCHY
            closest_match = next((k for k in MEDIAPIPE_HIERARCHY.keys() if marker.startswith(k)), None)
            if marker == closest_match or closest_match is None:
                continue
            # Create a new element in MEDIAPIPE_HIERARCHY with the info of the closest match
            MEDIAPIPE_HIERARCHY[marker] = deepcopy(MEDIAPIPE_HIERARCHY[closest_match])

            # Get the base children markers
            base_children_markers = MEDIAPIPE_HIERARCHY[closest_match]['children']
            
            # Change the values of the children with their closest match
            modified_children = []
            for child in base_children_markers:
                modified_children.append(next((k for k in markers.keys() if k.startswith(child)), None))
            MEDIAPIPE_HIERARCHY[marker]['children'] = modified_children

            # Remove the closest match from MEDIAPIPE_HIERARCHY
            del MEDIAPIPE_HIERARCHY[closest_match]

        # Iterate through each frame of the scene
        for frame in range (scene.frame_start, scene.frame_end):

            # Calculate the hand axes as a starting point.
            # TODO: Extend the function to start from the pelvis bone
            for side in ['left', 'right']:
                side_initial = side[0].upper()
                
                hand_y_axis = (
                    Vector(markers[VirtualBones['hand.' + side_initial].tail]['fcurves'][:, frame])
                    - Vector(markers[VirtualBones['hand.' + side_initial].head]['fcurves'][:, frame])
                )

                # Get the hand_locked_track_marker as the best match of markers.keys()
                hand_locked_track_marker = next((k for k in markers.keys() if k.startswith(side + '_' + hand_locked_track_marker_name)), None)

                hand_to_locked_track_marker = (
                    Vector(markers[hand_locked_track_marker]['fcurves'][:, frame])
                    - Vector(markers[VirtualBones['hand.' + side_initial].head]['fcurves'][:, frame])
                )

                # hand_z_axis as the projection of hand_to_thumb_cmc onto hand_y_axis
                hand_z_axis = (
                    hand_to_locked_track_marker
                    - hand_y_axis
                    * (
                        hand_y_axis.dot(hand_to_locked_track_marker)
                        / hand_y_axis.length_squared
                    )
                )

                # x_axis as the orthogonal vector of the y_axis and z_axis
                hand_x_axis = Vector(hand_y_axis.cross(hand_z_axis))

                # Save the vectors in the VirtualBones dictionary
                VirtualBones['hand.' + side_initial].bone_x_axis = Vector(hand_x_axis)
                VirtualBones['hand.' + side_initial].bone_y_axis = Vector(hand_y_axis)
                VirtualBones['hand.' + side_initial].bone_z_axis = Vector(hand_z_axis)

            # Iterate through the virtual bones dictionary and add constraints if the bone has the finger category
            for bone in VirtualBones:

                # If the bone has the hands or fingers category then calculate its origin axes based on its parent bone's axes
                if VirtualBones[bone].category in ['palm', 'proximal_phalanx', 'intermediate_phalanx', 'distal_phalanx']:

                    bone_head_position = Vector(markers[VirtualBones[bone].head]['fcurves'][:, frame])
                    bone_tail_position = Vector(markers[VirtualBones[bone].tail]['fcurves'][:, frame])

                    # If the bone is an index, ring or pinky metacarpal then adjust its head marker position
                    if bone in {'palm.01.L', 'palm.01.R', 'palm.03.L', 'palm.03.R', 'palm.04.L', 'palm.04.R'}:
                    # if bone in {'palm.01.R', 'palm.03.R', 'palm.04.R'} and frame == 316:
                        bone_head_position = compute_new_metacarpal_head(
                            metacarpal_head=bone_head_position,
                            metacarpal_tail=bone_tail_position,
                            reference_head=Vector(markers[VirtualBones[VirtualBones[bone].parent_bone].head]['fcurves'][:, frame]),
                            reference_tail=Vector(markers[VirtualBones[VirtualBones[bone].parent_bone].tail]['fcurves'][:, frame]),
                            new_head_metacarpal_ratio=VirtualBones[bone].new_head_metacarpal_ratio,
                            angle_offset=VirtualBones[bone].angle_offset,
                        )

                    # Calculate the bone's y axis
                    bone_y_axis = (
                        bone_tail_position
                        - bone_head_position
                    )

                    # Get the bone axes from its parent
                    bone_axes_from_parent = calculate_bone_axes_from_parent(
                        bone_y_axis,
                        [
                            Vector(VirtualBones[VirtualBones[bone].parent_bone].bone_x_axis),
                            Vector(VirtualBones[VirtualBones[bone].parent_bone].bone_y_axis),
                            Vector(VirtualBones[VirtualBones[bone].parent_bone].bone_z_axis)
                        ],
                    )

                    # Save the vectors in the virtual_bones dictionary
                    VirtualBones[bone].bone_x_axis = bone_axes_from_parent[0]
                    VirtualBones[bone].bone_y_axis = bone_axes_from_parent[1]
                    VirtualBones[bone].bone_z_axis = bone_axes_from_parent[2]

                    # If the bone has the target category then calculate its
                    # origin axes based on its parent bone's axes and rotate
                    # the tail empty (and its children) to meet the constraints
                    if VirtualBones[bone].category in target_categories:
                        for axis in ['x', 'z']:
                            # Get the min and max rotation limits based on the range of motion scale
                            axis_rotation_limit_min = getattr(VirtualBones[bone], f'{axis}_rotation_limit_min')
                            axis_rotation_limit_max = getattr(VirtualBones[bone], f'{axis}_rotation_limit_max')
                            range_of_motion = axis_rotation_limit_max - axis_rotation_limit_min
                            scaled_range_of_motion = range_of_motion * range_of_motion_scale
                            scaled_rotation_limit_min = max(-180, axis_rotation_limit_min + ((range_of_motion - scaled_range_of_motion) / 2))
                            scaled_rotation_limit_max = min(180, axis_rotation_limit_max - ((range_of_motion - scaled_range_of_motion) / 2))
                            
                            # Get the rotation delta of the bone axis
                            rotation_delta = get_bone_axis_rotation_delta(
                                bone_axis=getattr(VirtualBones[bone], f'bone_{axis}_axis'),
                                parent_bone_axis=Vector(getattr(VirtualBones[VirtualBones[bone].parent_bone], f'bone_{axis}_axis')),
                                parent_bone_ort_axis=Vector(getattr(VirtualBones[VirtualBones[bone].parent_bone], f'bone_{"z" if axis == "x" else "x"}_axis')),
                                axis_rotation_limit_min=scaled_rotation_limit_min,
                                axis_rotation_limit_max=scaled_rotation_limit_max,
                            )

                            if rotation_delta != 0:
                                # Calculate the rotation matrix axis as the cross product of the bone and parent axes
                                matrix_axis = Vector((getattr(VirtualBones[VirtualBones[bone].parent_bone], f'bone_{axis}_axis')).cross(getattr(VirtualBones[bone], f'bone_{axis}_axis')))
                                matrix_axis.normalize()

                                # Get the rotation matrix
                                rotation_matrix = Matrix.Rotation(rotation_delta, 4, matrix_axis.to_3d())

                                # Rotate the virtual bone tail empty
                                rotate_marker_around_pivot(
                                    marker=VirtualBones[bone].tail,
                                    pivot=Vector(markers[VirtualBones[bone].head]['fcurves'][:, frame]),
                                    rotation_matrix=rotation_matrix,
                                    frame=frame,
                                    markers_fcurves=markers,
                                    mediapipe_hierarchy=MEDIAPIPE_HIERARCHY
                                )

                                # Recalculate the bone y axis
                                bone_y_axis = (
                                    Vector(markers[VirtualBones[bone].tail]['fcurves'][:, frame])
                                    - Vector(markers[VirtualBones[bone].head]['fcurves'][:, frame])
                                )

                                # Get the bone axes from its parent
                                bone_axes_from_parent = calculate_bone_axes_from_parent(
                                    bone_y_axis,
                                    [
                                        Vector(VirtualBones[VirtualBones[bone].parent_bone].bone_x_axis),
                                        Vector(VirtualBones[VirtualBones[bone].parent_bone].bone_y_axis),
                                        Vector(VirtualBones[VirtualBones[bone].parent_bone].bone_z_axis)
                                    ],
                                )

                                # Save the vectors in the virtual_bones dictionary
                                VirtualBones[bone].bone_x_axis = bone_axes_from_parent[0]
                                VirtualBones[bone].bone_y_axis = bone_axes_from_parent[1]
                                VirtualBones[bone].bone_z_axis = bone_axes_from_parent[2]

        # Write the markers dictionary fcurve data to the objects fcurves
        for marker_name, marker_data in markers.items():
            for axis_idx in range(3):
                fcurve = marker_data['object'].animation_data.action.fcurves.find("location", index=axis_idx)

                # Create a flattened array of [frame0, value0, frame1, value1, ...]
                co = np.empty(2 * len(marker_data['fcurves'][axis_idx]), dtype=np.float32)
                co[0::2] = np.arange(len(marker_data['fcurves'][axis_idx]))  # Frame numbers
                co[1::2] = marker_data['fcurves'][axis_idx]  # Axis values

                # Assign all keyframes at once
                fcurve.keyframe_points.foreach_set("co", co)
                fcurve.update()  # Finalize changes

        return {'FINISHED'}
    
# TODO: Move these functions to a separate module,
# an scpecific module for limit markers range of motion or a general one
# like utilities
def calculate_bone_axes_from_parent(
    bone_y_axis: Vector,
    parent_bone_axes: list[Vector, Vector, Vector],
) -> list[Vector, Vector, Vector]:

    # Calculate the difference between the bone's y axis and its parent bone's y axis
    rotation_quat = parent_bone_axes[1].rotation_difference(bone_y_axis)

    # Rotate the parent x and z axes to get the bones local x and z axes
    bone_x_axis = parent_bone_axes[0]
    bone_x_axis.rotate(rotation_quat)
    bone_z_axis = parent_bone_axes[2]
    bone_z_axis.rotate(rotation_quat)

    return [
        Vector(bone_x_axis),
        Vector(bone_y_axis),
        Vector(bone_z_axis)
    ]


def get_bone_axis_rotation_delta(
    bone_axis,
    parent_bone_axis,
    parent_bone_ort_axis,
    axis_rotation_limit_min,
    axis_rotation_limit_max,
) -> float:

    # Normalize the vectors
    bone_axis_normalized = bone_axis.normalized()
    parent_bone_axis_normalized = parent_bone_axis.normalized()
    
    # Calculate the dot product between the the bone axis and its parent bone axis
    dot_product = bone_axis_normalized.dot(parent_bone_axis_normalized)
    # Clamp the dot product to avoid numerical errors beyond the range of acos
    clamped_dot_product = max(min(dot_product, 1.0), -1.0)

    # Calculate the angle
    angle = m.acos(clamped_dot_product)

    # Calculate the cross product between the axis of the bone and its parent bone axis
    cross_product = Vector(parent_bone_axis_normalized.cross(bone_axis_normalized))

    # Calculate the dot product between the cross product and the parent orthogonal axis
    cross_dot_orthogonal = cross_product.dot(parent_bone_ort_axis)

    # If the dot product is negative then the rotation angle is negative
    if cross_dot_orthogonal < 0:
        angle = -angle
    
    # Check if the angle is within the rotation limit values.
    # If it is outside, rotate the bone tail empty around the cross product
    # so the angle is on the closest rotation limit.
    rot_delta = 0

    # Calculate the angle difference between the rotation limit and the x_angle
    if angle < m.radians(axis_rotation_limit_min):
        rot_delta = m.radians(axis_rotation_limit_min) - angle
    elif angle > m.radians(axis_rotation_limit_max):
        rot_delta = m.radians(axis_rotation_limit_max) - angle

    # Adjust the rotation delta according to the dot product
    if cross_dot_orthogonal < 0:
        rot_delta = -rot_delta

    return rot_delta


def rotate_marker_around_pivot(
    marker: str,
    pivot: Vector,
    rotation_matrix: Matrix,
    frame: int,
    markers_fcurves: dict,
    mediapipe_hierarchy: dict,
):
    marker_global_position = Vector(markers_fcurves[marker]['fcurves'][:, frame])
    marker_pivot_vector = marker_global_position - pivot
    rotated_marker_pivot_vector = rotation_matrix @ marker_pivot_vector
    marker_new_global_position = pivot + rotated_marker_pivot_vector

    # Update the marker fcurve
    markers_fcurves[marker]['fcurves'][:, frame] = marker_new_global_position[:]

    # If marker has children then call this function for every child
    if marker in mediapipe_hierarchy and mediapipe_hierarchy[marker]['children']:
        for child in mediapipe_hierarchy[marker]['children']:
            rotate_marker_around_pivot(
                marker=child,
                pivot=pivot,
                rotation_matrix=rotation_matrix,
                frame=frame,
                markers_fcurves=markers_fcurves,
                mediapipe_hierarchy=mediapipe_hierarchy
            )

    return

# Function to get the correct head position of the metacarpals
def compute_new_metacarpal_head(
    metacarpal_head: Vector,
    metacarpal_tail: Vector,
    reference_head: Vector,
    reference_tail: Vector,
    new_head_metacarpal_ratio: float,
    angle_offset: float
) -> Vector:

    # Current and reference vectors
    current_metacarpal_vector = (metacarpal_tail - metacarpal_head).normalized()
    reference_vector = (reference_tail - reference_head).normalized()

    # Plane normal between them
    rotation_plane_normal = reference_vector.cross(current_metacarpal_vector).normalized()

    # Vector scaled by ratio
    rotating_vector = (metacarpal_tail - metacarpal_head) * new_head_metacarpal_ratio

    # Rotate by angle_offset around the plane normal
    angle_offset_rad = m.radians(angle_offset)
    rotation_matrix = Matrix.Rotation(angle_offset_rad, 4, rotation_plane_normal)
    rotated_vector = rotation_matrix @ rotating_vector

    # New head position
    return metacarpal_head + rotated_vector
