import time
import os
from pathlib import Path
from mathutils import Vector
from math import radians, atan, sqrt
import random
import bpy
import cv2

from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler

from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
    LENS_FOVS,
    RENDER_PARAMETERS,
)

from ajc27_freemocap_blender_addon.data_models.create_video.visual_components import (
    frame_number,
    logo,
    recording_parameters,
    mediapipe_skeleton_segment_lengths,
    plot_com_bos,
    plot_foot_deviation,
)

from ajc27_freemocap_blender_addon.data_models.create_video.frame_information import (
    frame_information
)

def create_video(
    handler: FreemocapDataHandler,
    scene: bpy.types.Scene,
    recording_folder: str,
    start_frame: int,
    end_frame: int,
    export_profile: str = 'showcase',
) -> None:

    # Place the required cameras
    cameras_positions = place_cameras(scene, export_profile)

    # Place the required lights
    place_lights(scene, cameras_positions)

    # Rearrange the background videos
    rearrange_background_videos(scene, videos_x_separation=0.1)

    set_render_elements(export_profile=export_profile)

    if export_profile in ['showcase']:
        add_background(scene)

    # Set the rendering properties
    set_rendering_properties()

    # Set the render resolution based on the export profile
    bpy.context.scene.render.resolution_x = EXPORT_PROFILES[export_profile]['resolution_x']
    bpy.context.scene.render.resolution_y = EXPORT_PROFILES[export_profile]['resolution_y']

    # Set the output file name
    video_file_name = Path(recording_folder).name + '.mp4'
    # Set the output file
    video_render_path = str(Path(recording_folder) / video_file_name)
    bpy.context.scene.render.filepath = video_render_path
    print(f"Exporting video to: {video_render_path} ...")

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Render the animation
    bpy.ops.render.render(animation=True)

    # Reset the scene defaults
    reset_scene_defaults()

    # Add the visual components
    add_visual_components(render_path=video_render_path,
                          file_directory=recording_folder,
                          export_profile=export_profile,
                          start_frame=start_frame,
                          handler=handler
    )

    if  Path(video_render_path).exists():
        print(f"Video file successfully created at: {video_render_path}")
    else:
        print("ERROR - Video file was not created!! Nothing found at:  {video_render_path} ")


def place_cameras(
    scene: bpy.types.Scene=None,
    export_profile: str='debug'
) -> list:
    
    camera_horizontal_fov = LENS_FOVS['50mm']['horizontal_fov']
    camera_vertical_fov = LENS_FOVS['50mm']['vertical_fov']

    # Camera angle margin to show more area than the capture movement
    angle_margin = 0.9

    # List of cameras positions
    cameras_positions = []

    # Create the camera
    camera_data = bpy.data.cameras.new(name="Front_Camera")
    camera = bpy.data.objects.new(name="Front_Camera", object_data=camera_data)
    scene.collection.objects.link(camera)

    # Assign the camera to the scene
    scene.camera = camera

    # Set the starting extreme points
    highest_point = Vector([0, 0, 0])
    lowest_point = Vector([0, 0, 0])
    leftmost_point = Vector([0, 0, 0])
    rightmost_point = Vector([0, 0, 0])

    # Find the extreme points as the highest, lowest, leftmost,
    # and rightmost considering all the frames
    for frame in range (scene.frame_start, scene.frame_end):
        
        scene.frame_set(frame)

        for object in scene.objects:
            if (object.type == 'EMPTY'
                and object.name not in (
                    'freemocap_origin_axes',
                    'world_origin',
                    'center_of_mass_data_parent',
                    'head',
                )
            ):
                if object.matrix_world.translation[2] > highest_point[2]:
                    highest_point = object.matrix_world.translation.copy()
                if object.matrix_world.translation[2] < lowest_point[2]:
                    lowest_point = object.matrix_world.translation.copy()
                if object.matrix_world.translation[0] < leftmost_point[0]:
                    leftmost_point = object.matrix_world.translation.copy()
                if object.matrix_world.translation[0] > rightmost_point[0]:
                    rightmost_point = object.matrix_world.translation.copy()

    # Draw the extreme points as mesh spheres
    # bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, enter_editmode=False, align='WORLD', location=highest_point, scale=(1, 1, 1))
    # bpy.data.objects['Sphere'].name = 'highest_point'
    # bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, enter_editmode=False, align='WORLD', location=lowest_point, scale=(1, 1, 1))
    # bpy.data.objects['Sphere'].name = 'lowest_point'
    # bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, enter_editmode=False, align='WORLD', location=leftmost_point, scale=(1, 1, 1))
    # bpy.data.objects['Sphere'].name = 'leftmost_point'
    # bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, enter_editmode=False, align='WORLD', location=rightmost_point, scale=(1, 1, 1))
    # bpy.data.objects['Sphere'].name = 'rightmost_point'
            
    # Calculate the position of the camera assuming is centered at 0 on the x axis and pointing towards the y axis
    # and covers the extreme points including a margin

    # Camera distances to just cover the leftmost and rightmost points
    camera_y_axis_distance_leftmost = (
        leftmost_point[1]
        - abs(leftmost_point[0])
        / atan(radians(camera_horizontal_fov * angle_margin / 2))
    )
    camera_y_axis_distance_rightmost = (
        rightmost_point[1]
        - abs(rightmost_point[0])
        / atan(radians(camera_horizontal_fov * angle_margin / 2))
    )

    # Camera distances to just cover the highest and lowest points
    # considering its centered between the two points on the z axis
    camera_y_axis_distance_highest = (
        highest_point[1]
        - ((highest_point[2] - lowest_point[2]) / 2)
        / atan(radians(camera_vertical_fov * angle_margin / 2))
    )
    camera_y_axis_distance_lowest = (
        lowest_point[1]
        - ((highest_point[2] - lowest_point[2]) / 2)
        / atan(radians(camera_vertical_fov * angle_margin / 2))
    )

    # Calculate the final y position of the camera as the minimum distance
    camera_y_axis_distance = min(camera_y_axis_distance_leftmost,
                                 camera_y_axis_distance_rightmost,
                                 camera_y_axis_distance_highest,
                                 camera_y_axis_distance_lowest)

    camera.location = (
        0,
        camera_y_axis_distance,
        highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
    )
    camera.rotation_euler = (radians(90), 0, 0)

    # Add the camera position to the cameras position list
    cameras_positions.append(camera.location)

    return cameras_positions

def place_lights(
    scene: bpy.types.Scene=None,
    cameras_positions: list=None
) -> None:

    # Lights vertical offset in Blender units
    lights_vertical_offset = 2

    # Create the light
    light_data = bpy.data.lights.new(name="Front_Light", type='SPOT')
    light = bpy.data.objects.new(name="Front_Light", object_data=light_data)
    scene.collection.objects.link(light)

    # Set the strength of the light
    light.data.energy = (
        200
        * sqrt(lights_vertical_offset**2 + cameras_positions[0][1]**2)
    )

    # Set the location of the light
    light.location = (cameras_positions[0][0],
                      cameras_positions[0][1],
                      cameras_positions[0][2] + lights_vertical_offset
    )

    # Set the rotation of the light so it points to the point
    # (0, 0, cameras_positions[0][2])
    light.rotation_euler = (
        atan(abs(cameras_positions[0][1]) / lights_vertical_offset),
        0,
        0
    )

    return

def rearrange_background_videos(
    scene: bpy.types.Scene=None,
    videos_x_separation: float=0.1
) -> None:

    # Create a list with the background videos
    background_videos = []

    # Append the background videos to the list
    for object in scene.objects:
        if 'video_' in object.name:
            background_videos.append(object)

    # Get the videos x dimension
    videos_x_dimension = background_videos[0].dimensions.x

    # Calculate the first video x position (from the left to the right)
    first_video_x_position = (
        -(len(background_videos) - 1)
        / 2 * (videos_x_dimension + videos_x_separation)
    )

    # Iterate through the background videos
    for video_index in range(len(background_videos)):
        # Set the location of the video
        background_videos[video_index].location[0] = (
            first_video_x_position
            + video_index
            * (videos_x_dimension + videos_x_separation)
        )

    return

def add_background(
    scene: bpy.types.Scene=None,
) -> None:
    
    # Create the background material
    background_material = bpy.data.materials.new(name="Background_Material")
    background_material.use_nodes = True

    # Get the material node tree
    material_node_tree = background_material.node_tree

    # Create the texture node
    texture_node = material_node_tree.nodes.new(type="ShaderNodeTexGradient")
    texture_node.gradient_type = 'SPHERICAL'

    # Link the node to the material
    material_node_tree.links.new(texture_node.outputs["Color"], material_node_tree.nodes["Principled BSDF"].inputs["Base Color"])

    # Add a plane mesh
    bpy.ops.mesh.primitive_plane_add(
        enter_editmode=False,
        align='WORLD',
        size=10.0,
        location=(0, 4.3, 0),
        rotation=(radians(90), 0, 0),
        scale=(1, 1, 1)
    )

    # Change the name of the plane mesh
    bpy.context.active_object.name = "background"

    #  Get reference to the plane mesh
    background = bpy.data.objects["background"]

    # Select the mesh
    background.select_set(True)
    bpy.context.view_layer.objects.active = background

    # Add a geometry node to the angle mesh
    bpy.ops.node.new_geometry_nodes_modifier()

    # Change the name of the geometry node
    background.modifiers[0].name = "Geometry_Nodes_Background"

    # Get the node tree and change its name
    node_tree = bpy.data.node_groups[0]
    node_tree.name = "Geometry_Nodes_Background"

    # Get the Input and Output nodes
    input_node = node_tree.nodes["Group Input"]
    input_node.location = (-600, 300)
    output_node = node_tree.nodes["Group Output"]
    output_node.location = (1200, 300)

    # Add the modification nodes
    subdivide_mesh_node = node_tree.nodes.new(type='GeometryNodeSubdivideMesh')
    subdivide_mesh_node.inputs[1].default_value = 6
    triangulate_node = node_tree.nodes.new(type='GeometryNodeTriangulate')
    triangulate_node.location = (200, 300)

    combine_xyz_node = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz_node.location = (-200, -300)
    random_x_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
    random_y_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
    random_z_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
    random_x_node.location = (-500, -300)
    random_y_node.location = (-500, -500)
    random_z_node.location = (-500, -700)

    # Set min and max values
    random_x_node.inputs[2].default_value = -0.01
    random_y_node.inputs[2].default_value = -0.01
    random_z_node.inputs[2].default_value = 0
    random_x_node.inputs[3].default_value = 0.01
    random_y_node.inputs[3].default_value = 0.01
    random_z_node.inputs[3].default_value = 0.3
    # Set the random seed values
    random_x_node.inputs[8].default_value = random.randrange(0, 100)
    random_y_node.inputs[8].default_value = random.randrange(0, 100)
    random_z_node.inputs[8].default_value = random.randrange(0, 100)
    # Connect the random nodes
    node_tree.links.new(random_x_node.outputs[1], combine_xyz_node.inputs['X'])
    node_tree.links.new(random_y_node.outputs[1], combine_xyz_node.inputs['Y'])
    node_tree.links.new(random_z_node.outputs[1], combine_xyz_node.inputs['Z'])

    dual_mesh_node = node_tree.nodes.new(type='GeometryNodeDualMesh')
    dual_mesh_node.location = (400, 300)

    transform_node = node_tree.nodes.new(type='GeometryNodeTransform')
    transform_node.inputs[2].default_value[2] = 0.785398
    transform_node.inputs[3].default_value[0] = 3
    transform_node.inputs[3].default_value[1] = 3
    transform_node.location = (600, 300)

    extrude_mesh_node = node_tree.nodes.new(type='GeometryNodeExtrudeMesh')
    extrude_mesh_node.location = (800, 300)

    set_material_node = node_tree.nodes.new(type='GeometryNodeSetMaterial')
    set_material_node.inputs[2].default_value = bpy.data.materials["Background_Material"]
    set_material_node.location = (1000, 300)

    # Connect the nodes
    node_tree.links.new(input_node.outputs["Geometry"], subdivide_mesh_node.inputs["Mesh"])
    node_tree.links.new(subdivide_mesh_node.outputs["Mesh"], triangulate_node.inputs["Mesh"])
    node_tree.links.new(triangulate_node.outputs["Mesh"], dual_mesh_node.inputs["Mesh"])
    node_tree.links.new(dual_mesh_node.outputs["Dual Mesh"], transform_node.inputs["Geometry"])
    node_tree.links.new(transform_node.outputs["Geometry"], extrude_mesh_node.inputs["Mesh"])
    node_tree.links.new(combine_xyz_node.outputs["Vector"], extrude_mesh_node.inputs["Offset"])
    node_tree.links.new(extrude_mesh_node.outputs["Mesh"], set_material_node.inputs["Geometry"])
    node_tree.links.new(set_material_node.outputs["Geometry"], output_node.inputs["Geometry"])

    return

def set_rendering_properties() -> None:

    # Set the rendering properties
    for key, value in RENDER_PARAMETERS.items():

        # Split the key into context and property names
        key_parts = key.split(".")

        # Start with the bpy.context object
        context = bpy.context

        # Traverse through the key parts to access the correct context and property
        for part in key_parts[:-1]:
            context = getattr(context, part)

        # Set the property
        setattr(context, key_parts[-1], value)

    return

def set_render_elements(
    export_profile: str='debug',
) -> None:
    
    def set_hide_render_recursive(obj):
        obj.hide_render = False
        for child in obj.children:
            set_hide_render_recursive(child)

    # Set hide_render equal to True for all the objects
    for obj in bpy.data.objects:
        if obj.name not in ['Front_Camera', 'Front_Light']:
            obj.hide_render = True

    # Set hide_render equal to False for the render elements
    for obj in bpy.data.objects:
        # if any(obj.name in element for element in EXPORT_PROFILES[export_profile]['render_elements']):
        if any(element in obj.name for element in EXPORT_PROFILES[export_profile]['render_elements']):
            print("Setting Render Hide: " + obj.name)
            set_hide_render_recursive(obj)

    return

def reset_scene_defaults() -> None:

    # Enable all elements in render
    for obj in bpy.data.objects:
        obj.hide_render = False

    # Hide the background if present
    if bpy.data.objects["background"] is not None:
        bpy.data.objects["background"].hide_set(True)    

def add_visual_components(
    render_path: str,
    file_directory: Path,
    export_profile: str='debug',
    start_frame: int=0,
    handler: FreemocapDataHandler=None,
) -> None:

    # Get a reference to the render
    video = cv2.VideoCapture(render_path)

    # Create a VideoWriter object to write the output frames
    output_writer = cv2.VideoWriter(
        (os.path.dirname(render_path)
        + '/' + os.path.basename(render_path)[:-4]
        + '_' + export_profile + '.mp4'),
        cv2.VideoWriter_fourcc(*'mp4v'),
        RENDER_PARAMETERS['scene.render.fps'],
        (EXPORT_PROFILES[export_profile]['resolution_x'],
         EXPORT_PROFILES[export_profile]['resolution_y']),
         EXPORT_PROFILES[export_profile]['bitrate'],
    )
    
    # Create new frame_info object
    frame_info = frame_information(
        file_directory=str(file_directory),
        width=EXPORT_PROFILES[export_profile]['resolution_x'],
        height=EXPORT_PROFILES[export_profile]['resolution_y'],
        total_frames=int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
        frame_start=start_frame,
        handler=handler,
    )

    # Creat the visual component objects list
    visual_components_list = []
    for visual_component in EXPORT_PROFILES[export_profile]['visual_components']:
        visual_component_class = globals()[visual_component]
        visual_components_list.append(visual_component_class(frame_info))

    index_frame = 0
    # Add the logo to the video
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        # Update the frame number in frame_info
        frame_info.frame_number = index_frame

        # Add each visual component
        for visual_component in visual_components_list:
            frame = visual_component.add_component(frame, frame_info)

        # Write the frame
        output_writer.write(frame)

        index_frame += 1

    video.release()
    output_writer.release()
    cv2.destroyAllWindows()

    return
