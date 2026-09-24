import bpy

from freemocap_blender_addon.utilities.get_fcurves_from_object_action import (
    get_fcurves_from_object_action,
)

from freemocap_blender_addon.data_models.bones.bone_definitions import _BONE_DEFINITIONS
from freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy


class FREEMOCAP_OT_limit_markers_range_of_motion(bpy.types.Operator):
    bl_idname = 'freemocap._limit_markers_range_of_motion'
    bl_label = 'Limit Markers Range of Motion'
    bl_description = "Limit Markers Range of Motion"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Limiting Markers Range of Motion.......")

        scene = context.scene
        props = context.scene.freemocap_ui_properties.limit_markers_range_of_motion_properties

        # Get the top-level parent empty that contains all marker empties
        data_parent_empty = bpy.data.objects[
            context.scene.freemocap_properties.scope_data_parent
        ]

        # Frame Range
        start_frame = context.scene.frame_start
        end_frame = context.scene.frame_end

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

        limit_markers_range_of_motion(
            data_parent_empty=data_parent_empty,
            start_frame=start_frame,
            end_frame=end_frame,
            target_categories=target_categories,
            range_of_motion_scale=range_of_motion_scale,
            hand_locked_track_marker_name=hand_locked_track_marker_name,
            hand_damped_track_marker_name=hand_damped_track_marker_name,
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
                        fcurves = get_fcurves_from_object_action(marker)
                        if fcurves is None:
                            continue

                        # Get the position fcurves
                        fcurve_x = fcurves.find("location", index=0)
                        fcurve_y = fcurves.find("location", index=1)
                        fcurve_z = fcurves.find("location", index=2)

                        if fcurve_x is None or fcurve_y is None or fcurve_z is None:
                            continue

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
            marker_obj = marker_data['object']
            fcurves = get_fcurves_from_object_action(marker_obj)
            if fcurves is None:
                continue

            for axis_idx in range(3):
                fcurve = fcurves.find("location", index=axis_idx)
                if fcurve is not None:
                    # Create a flattened array of [frame0, value0, frame1, value1, ...]
                    co = np.empty(2 * len(marker_data['fcurves'][axis_idx]), dtype=np.float32)
                    co[0::2] = np.arange(len(marker_data['fcurves'][axis_idx]))  # Frame numbers
                    co[1::2] = marker_data['fcurves'][axis_idx]  # Axis values
    
                    # Assign all keyframes at once
                    fcurve.keyframe_points.foreach_set("co", co)
                    fcurve.update()  # Finalize changes

        return {'FINISHED'}
