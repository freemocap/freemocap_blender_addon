import bpy
from pathlib import Path
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
)

def composite_video(
    scene: bpy.types.Scene,
    recording_folder: str,
    export_profile: str = 'debug',
) -> None:
    
    # Set up compositor
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    # Clear existing nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # Create a dictionary to store the render camera nodes
    render_camera_nodes = []
    render_cameras_count = len(EXPORT_PROFILES[export_profile]['render_cameras'])

    # For each render camera create MovieClip, Scale and Translate nodes
    for index, camera in enumerate(EXPORT_PROFILES[export_profile]['render_cameras']):

        #  Get a reference to the render_camera
        render_camera = EXPORT_PROFILES[export_profile]['render_cameras'][camera]

        # Get the render camera file name
        render_camera_filename = Path(recording_folder).name + '_' + camera + '.mp4'
        render_camera_filepath = str(Path(recording_folder) / 'video_export' / 'render_cameras' / render_camera_filename)

        # Create MovieClip node
        video_node = tree.nodes.new(type="CompositorNodeMovieClip")
        video_node.clip = bpy.data.movieclips.load(render_camera_filepath)
        
        #  Set the node position
        video_node.location = (-800, (render_cameras_count - index) * 300)

        # Create Scale node
        scale_node = tree.nodes.new(type="CompositorNodeScale")
        scale_node.space = render_camera['scale_space']
        scale_node.inputs[1].default_value = render_camera['scale_x']
        scale_node.inputs[2].default_value = render_camera['scale_y']
        scale_node.location = (-600, (render_cameras_count - index) * 300)

        # Create Translate node
        translate_node = tree.nodes.new(type="CompositorNodeTranslate")
        translate_node.use_relative = render_camera['translate_relative']
        translate_node.inputs[1].default_value = render_camera['translate_x']
        translate_node.inputs[2].default_value = render_camera['translate_y']
        translate_node.location = (-400, (render_cameras_count - index) * 300)

        # Link nodes
        links.new(video_node.outputs[0], scale_node.inputs[0])
        links.new(scale_node.outputs[0], translate_node.inputs[0])

        # Store the last node as the render camera node
        render_camera_nodes.append(translate_node)

    # If the render cameras are more than one, then combine them using Alpha
    # Over nodes
    cameras_alpha_over_nodes = []
    for i in range(0, len(render_camera_nodes) - 1):
        
        # If the cameras_alpha_over_nodes is empty
        if not cameras_alpha_over_nodes:
            # Connect the first two render cameras to the first AlphaOver node
            cameras_alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            cameras_alpha_over_nodes[i].location = (
                -200,
                (render_cameras_count - i - 1) * 300
            )
            # Link nodes
            links.new(
                render_camera_nodes[i].outputs[0],
                cameras_alpha_over_nodes[i].inputs[1]
            )
            links.new(
                render_camera_nodes[i+1].outputs[0],
                cameras_alpha_over_nodes[i].inputs[2]
            )

        else:
            # Connect render camera and previous alpha over node to next alpha over node
            cameras_alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            cameras_alpha_over_nodes[i].location = (
                -200,
                (render_cameras_count - i - 1) * 300
            )
            # Link nodes
            links.new(
                cameras_alpha_over_nodes[i-1].outputs[0],
                cameras_alpha_over_nodes[i].inputs[1]
            )
            links.new(
                render_camera_nodes[i+1].outputs[0],
                cameras_alpha_over_nodes[i].inputs[2]
            )

    # Create a dictionary to store the overlay nodes
    overlay_nodes = []
    overlays_count = len(EXPORT_PROFILES[export_profile]['overlays'])

    # For each overlay create the corresponding node
    for index, overlay in enumerate(EXPORT_PROFILES[export_profile]['overlays']):

        # Get a reference to the overlay object
        overlay_dict = EXPORT_PROFILES[export_profile]['overlays'][overlay]

        if overlay_dict['type'] == 'image':
            # Create Image node
            overlay_node = tree.nodes.new(type="CompositorNodeImage")
            overlay_node.image = bpy.data.images.load(overlay_dict['path'])
            overlay_node.location = (
                -800,
                -(overlays_count - index - 1) * 400 - 50
            )
        elif overlay_dict['type'] == 'image_sequence':
            overlay_node = tree.nodes.new(type="CompositorNodeImage")
            plot_image = bpy.data.images.load(str(Path(recording_folder) / overlay_dict['path']))
            plot_image.source = 'SEQUENCE'
            overlay_node.image = plot_image
            overlay_node.frame_duration = scene.frame_end - scene.frame_start

        # Create Scale node
        scale_node = tree.nodes.new(type="CompositorNodeScale")
        scale_node.space = overlay_dict['scale_space']
        scale_node.inputs[1].default_value = overlay_dict['scale_x']
        scale_node.inputs[2].default_value = overlay_dict['scale_y']
        scale_node.location = (
            -600,
            -(overlays_count - index - 1) * 400 - 50
        )

        # Create Translate node
        translate_node = tree.nodes.new(type="CompositorNodeTranslate")
        translate_node.use_relative = overlay_dict['translate_relative']
        translate_node.inputs[1].default_value = overlay_dict['translate_x']
        translate_node.inputs[2].default_value = overlay_dict['translate_y']
        translate_node.location = (
            -400,
            -(overlays_count - index - 1) * 400 - 50
        )

        # Link nodes
        links.new(overlay_node.outputs[0], scale_node.inputs[0])
        links.new(scale_node.outputs[0], translate_node.inputs[0])

        # Store the last node as the overlay node
        overlay_nodes.append(translate_node)

    # If the overlays are more than one, then combine them using Alpha
    # Over nodes
    overlays_alpha_over_nodes = []
    for i in range(0, len(overlay_nodes) - 1):
        
        # If the overlays_alpha_over_nodes is empty
        if not overlays_alpha_over_nodes:
            # Connect the first two overlays to the first AlphaOver node
            overlays_alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            overlays_alpha_over_nodes[i].location = (
                -200,
                -(overlays_count - i - 2) * 400 - 50
            )
            # Link nodes
            links.new(
                overlay_nodes[i].outputs[0],
                overlays_alpha_over_nodes[i].inputs[2]
            )
            links.new(
                overlay_nodes[i+1].outputs[0],
                overlays_alpha_over_nodes[i].inputs[1]
            )

        else:
            # Connect render camera and previous alpha over node to next alpha over node
            overlays_alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            overlays_alpha_over_nodes[i].location = (
                -200,
                -(overlays_count - i - 2) * 400 - 50
            )
            # Link nodes
            links.new(
                overlays_alpha_over_nodes[i-1].outputs[0],
                overlays_alpha_over_nodes[i].inputs[2]
            )
            links.new(
                overlay_nodes[i+1].outputs[0],
                overlays_alpha_over_nodes[i].inputs[1]
            )

    # Connect the cameras and overlays last nodes
    cameras_overlays_alpha_over_node = tree.nodes.new(type="CompositorNodeAlphaOver")
    cameras_overlays_alpha_over_node.location = (
        100,
        0
    )
    if render_cameras_count == 1:
        render_cameras_end_node = render_camera_nodes[0]
    else:
        render_cameras_end_node = cameras_alpha_over_nodes[-1]
    if overlays_count == 1:
        overlays_end_node = overlay_nodes[0]
    else:
        overlays_end_node = overlays_alpha_over_nodes[-1]

    links.new(
        render_cameras_end_node.outputs[0],
        cameras_overlays_alpha_over_node.inputs[1]
    )
    links.new(
        overlays_end_node.outputs[0],
        cameras_overlays_alpha_over_node.inputs[2]
    )

    # Set output node
    output_node = tree.nodes.new(type="CompositorNodeComposite")
    output_node.location = (
        300,
        0
    )
    # Connect cameras and overlays alpha over node to output node
    links.new(cameras_overlays_alpha_over_node.outputs[0], output_node.inputs[0])

    # Set render settings
    bpy.context.scene.render.resolution_x = EXPORT_PROFILES[export_profile]['resolution_x']
    bpy.context.scene.render.resolution_y = EXPORT_PROFILES[export_profile]['resolution_y']
    output_render_name = Path(recording_folder).name + '_' + export_profile + '.mp4'
    output_render_path = str(Path(recording_folder) / 'video_export' / output_render_name)
    bpy.context.scene.render.filepath = output_render_path

    # Render the animation
    bpy.ops.render.render(animation=True)

    return
