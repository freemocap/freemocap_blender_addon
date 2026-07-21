import bpy
import numpy as np
from mathutils import Vector, Matrix


def animate_angle_meshes(
    angle_values: np.ndarray,
    reference_vectors: np.ndarray,
    rotation_plane_normals: np.ndarray,
    angle_meshes: dict,
    angleText_meshes: dict,
    angle_text_orientation: str,
) -> None:

    for i, angle_mesh in enumerate(angle_meshes):
        #  Set a simple reference to the angle mesh
        obj = angle_meshes[angle_mesh]
        # Create an action and fcurves
        action = bpy.data.actions.new(name=f"{obj.name}_Action")
        obj.animation_data_create()
        obj.animation_data.action = action

        # If Blender version is >= 4.4, create the structure for the action
        if bpy.app.version >= (4, 4):
            slot = action.slots.new(id_type='OBJECT', name=obj.name)
            layer = action.layers.new("Layer")
            strip = layer.strips.new(type='KEYFRAME')
            channelbag = strip.channelbag(slot, ensure=True)
            obj.animation_data.action_slot = action.slots[0]

        # Precompute frames and locations
        num_frames = angle_values.shape[0]
        frames = np.arange(0, num_frames, dtype=np.float32)
        
        rotation_eulers = np.zeros((num_frames, 3))
        for frame in range(num_frames):

            # Get vectors and normalize
            z_axis = Vector(rotation_plane_normals[frame, i]).normalized()
            x_raw = Vector(reference_vectors[frame, i]).normalized()

            # Project x to be orthogonal to z (Gram-Schmidt)
            x_axis = (x_raw - z_axis * x_raw.dot(z_axis)).normalized()

            # Compute Y as Z × X (right-handed coordinate system)
            y_axis = z_axis.cross(x_axis).normalized()

            # Construct rotation matrix (X, Y, Z as columns)
            rot_matrix = Matrix((
                x_axis,
                y_axis,
                z_axis,
            )).transposed()  # Blender expects columns to be local axes

            # Convert to Euler
            rotation_eulers[frame] = rot_matrix.to_euler('XYZ')
            
        # For each axis (x, y, z), set keyframes in bulk
        for axis in range (0,3):

            # Create the euler_rotation fcurve
            if bpy.app.version >= (4, 4):
                fcurve = channelbag.fcurves.new(data_path="rotation_euler", index=axis)
            else:
                fcurve = action.fcurves.new(data_path="rotation_euler", index=axis)

            fcurve.keyframe_points.add(count=num_frames)

            # Create a flattened array of [frame0, value0, frame1, value1, ...]
            co = np.empty(2 * num_frames, dtype=np.float32)
            co[0::2] = frames  # Frame numbers
            co[1::2] = rotation_eulers[:, axis]  # Axis values

            # Assign all keyframes at once
            fcurve.keyframe_points.foreach_set("co", co)

            # Finalize changes
            fcurve.update()

        # Now animate the sweep angle property of the arc node of the mesh
        # Get geometry node modifier and arc node
        modifier = obj.modifiers[0]
        arc_node = modifier.node_group.nodes["Arc"]
        # Create a custom property to animate the sweep angle via driver
        prop_name = "arc_angle"
        if prop_name not in obj:
            obj[prop_name] = 0.0
            obj["_RNA_UI"] = obj.get("_RNA_UI", {})
            obj["_RNA_UI"][prop_name] = {"min": 0.0, "max": 6.28319, "description": "Arc angle in radians"}

        # Add driver to Arc input
        driver = arc_node.inputs[6].driver_add("default_value").driver
        driver.type = 'AVERAGE'
        var = driver.variables.new()
        var.name = 'arc_val'
        var.type = 'SINGLE_PROP'
        var.targets[0].id = obj
        var.targets[0].data_path = f'["{prop_name}"]'

        # Create fcurve for custom property (which controls the Arc input)
        if bpy.app.version >= (4, 4):
            prop_fcurve = channelbag.fcurves.new(data_path=f'["{prop_name}"]')
        else:
            prop_fcurve = action.fcurves.new(data_path=f'["{prop_name}"]')

        # Create a flattened array of [frame0, value0, frame1, value1, ...]
        prop_fcurve.keyframe_points.add(count=num_frames)
        co = np.empty(2 * num_frames, dtype=np.float32)
        co[0::2] = frames
        co[1::2] = np.deg2rad(angle_values[:, i].astype(np.float32))
        prop_fcurve.keyframe_points.foreach_set("co", co)
        prop_fcurve.update()

        # Animate the text mesh
        text_obj = angleText_meshes[angle_mesh]
        text_prop_name = "angle_value"

        if text_prop_name not in text_obj:
            text_obj[text_prop_name] = 0.0
            text_obj["_RNA_UI"] = text_obj.get("_RNA_UI", {})
            text_obj["_RNA_UI"][text_prop_name] = {
                "min": -180.0,
                "max": 180.0,
                "description": "Display angle in degrees"
            }

        # Add driver to Value to String input
        text_modifier = text_obj.modifiers[0]
        value_node = text_modifier.node_group.nodes["Value to String"]
        driver = value_node.inputs[0].driver_add("default_value").driver
        driver.type = 'AVERAGE'
        var = driver.variables.new()
        var.name = 'angle_val'
        var.type = 'SINGLE_PROP'
        var.targets[0].id = text_obj
        var.targets[0].data_path = f'["{text_prop_name}"]'

        # Create animation data for text mesh
        text_action = bpy.data.actions.new(name=f"{text_obj.name}_Action")
        text_obj.animation_data_create()
        text_obj.animation_data.action = text_action

        # If Blender version is >= 4.4, create the structure for the action
        if bpy.app.version >= (4, 4):
            slot = text_action.slots.new(id_type='OBJECT', name=text_obj.name)
            layer = text_action.layers.new("Layer")
            strip = layer.strips.new(type='KEYFRAME')
            channelbag = strip.channelbag(slot, ensure=True)
            text_obj.animation_data.action_slot = text_action.slots[0]

        # Add fcurve for animating the property
        if bpy.app.version >= (4, 4):
            text_fcurve = channelbag.fcurves.new(data_path=f'["{text_prop_name}"]')
        else:
            text_fcurve = text_action.fcurves.new(data_path=f'["{text_prop_name}"]')

        text_fcurve.keyframe_points.add(count=num_frames)

        # Use raw degrees, optionally rounded to 1 decimal
        text_degrees = np.round(angle_values[:, i].astype(np.float32), decimals=1)

        co = np.empty(2 * num_frames, dtype=np.float32)
        co[0::2] = frames
        co[1::2] = text_degrees
        text_fcurve.keyframe_points.foreach_set("co", co)
        text_fcurve.update()

        # Animate the text mesh rotation depending on the orientation option
        if angle_text_orientation == 'rotation_plane_normal':
            text_rotation_eulers = np.zeros((num_frames, 3))
            for frame in range(num_frames):
                normal = Vector(rotation_plane_normals[frame, i])
                z_angle = np.arctan2(normal.x, -normal.y)

                # Set the euler rotation, preserving the initial 90-degree X rotation.
                text_rotation_eulers[frame] = [np.pi / 2, 0, z_angle]

        elif angle_text_orientation == 'global_x':
            text_rotation_eulers = np.tile([np.pi / 2, 0, 0], (num_frames, 1))
        elif angle_text_orientation == 'global_y':
            text_rotation_eulers = np.tile([np.pi / 2, 0, np.pi / 2], (num_frames, 1))
        elif angle_text_orientation == 'global_z':
            text_rotation_eulers = np.tile([0, 0, 0], (num_frames, 1))
        elif angle_text_orientation == 'global_-x':
            text_rotation_eulers = np.tile([np.pi / 2, 0, np.pi], (num_frames, 1))
        elif angle_text_orientation == 'global_-y':
            text_rotation_eulers = np.tile([np.pi / 2, 0, -np.pi / 2], (num_frames, 1))
        elif angle_text_orientation == 'global_-z':
            text_rotation_eulers = np.tile([np.pi, 0, 0], (num_frames, 1))
        else:
            raise ValueError(f"Invalid angle text orientation: {angle_text_orientation}")        

        # For each axis (x, y, z), set keyframes in bulk for the text mesh rotation
        for axis in range(3):
            if bpy.app.version >= (4, 4):
                rot_fcurve = channelbag.fcurves.new(data_path="rotation_euler", index=axis)
            else:
                rot_fcurve = text_action.fcurves.new(data_path="rotation_euler", index=axis)

            rot_fcurve.keyframe_points.add(count=num_frames)

            co = np.empty(2 * num_frames, dtype=np.float32)
            co[0::2] = frames
            co[1::2] = text_rotation_eulers[:, axis]

            rot_fcurve.keyframe_points.foreach_set("co", co)
            rot_fcurve.update()

    return
