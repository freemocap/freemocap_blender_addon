import bpy
import re

def add_motion_path(
    context: bpy.context,
    data_object_basename: str,
    show_line: bool = True,
    line_thickness: int = 6,
    use_custom_color: bool = False,
    line_color: tuple = (1.0, 1.0, 1.0),
    line_color_post: tuple = (0.5, 0.5, 0.5),
    frames_before: int = 10,
    frames_after: int = 10,
    frame_step: int = 1,
    show_frame_numbers: bool = False,
    show_keyframes: bool = False,
    show_keyframe_number: bool = False
) -> None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get reference to the object
    data_parent_empty = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]
    data_object_name = None
    for child in data_parent_empty.children_recursive:
        if re.search(data_object_basename, child.name):
            data_object_name = child.name
            break
    if not data_object_name:
        raise ValueError(f'Object with name {data_object_basename} not found in children of `data_parent_empty`: {data_parent_empty.name}')

    obj = bpy.data.objects[data_object_name]

    # Select the object
    obj.select_set(True)

    # Set the object as active object
    bpy.context.view_layer.objects.active = obj

    # Calculate paths
    bpy.ops.object.paths_calculate(display_type='CURRENT_FRAME', range='SCENE')
    # Set motion path properties for the specific object
    if obj.motion_path:
        obj.motion_path.lines = show_line
        obj.motion_path.line_thickness = line_thickness
        obj.motion_path.use_custom_color = use_custom_color
        obj.motion_path.color = line_color
        obj.motion_path.color_post = line_color_post
        obj.animation_visualization.motion_path.frame_before = frames_before
        obj.animation_visualization.motion_path.frame_after = frames_after
        obj.animation_visualization.motion_path.frame_step = frame_step
        obj.animation_visualization.motion_path.show_frame_numbers = show_frame_numbers
        obj.animation_visualization.motion_path.show_keyframe_highlight = show_keyframes
        obj.animation_visualization.motion_path.show_keyframe_numbers = show_keyframe_number

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    return
