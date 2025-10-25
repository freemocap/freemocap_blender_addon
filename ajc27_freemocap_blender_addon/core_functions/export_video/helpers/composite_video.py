import bpy
from pathlib import Path
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
    RENDER_BACKGROUND,
)

def composite_video(
    scene: bpy.types.Scene,
    recording_folder: str,
    export_profile: dict,
    start_frame: int,
    end_frame: int
) -> None:
    
    # Get the total amount of frames to render
    total_render_frames = end_frame - start_frame

    # Set the start and end frames as one and total_render_frames as
    # The compositor plays movieclips from frame 1 instead of the
    # current frame
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_render_frames
    
    # Set up compositor
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    # Clear existing nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # Create a list of alpha over nodes
    alpha_over_nodes = []

    # Create the background nodes
    background_end_node = create_background_nodes(
        export_profile=export_profile,
        tree=tree,
        links=links,
    )

    # Create the render camera nodes
    create_camera_nodes(
        export_profile=export_profile,
        recording_folder=recording_folder,
        alpha_over_nodes=alpha_over_nodes,
        background_end_node=background_end_node,
        tree=tree,
        links=links,
    )

    # Create the overlay nodes
    create_overlay_nodes(
        scene=scene,
        export_profile=export_profile,
        recording_folder=recording_folder,
        alpha_over_nodes=alpha_over_nodes,
        background_end_node=background_end_node,
        tree=tree,
        links=links,
    )

    # Set output node
    output_node = tree.nodes.new(type="CompositorNodeComposite")
    output_node.location = (
        300,
        0
    )
    # Connect last alpha over node to output node
    if alpha_over_nodes:
        links.new(alpha_over_nodes[-1].outputs[0], output_node.inputs[0])
    else:
        links.new(background_end_node.outputs[0], output_node.inputs[0])

    # Set render settings
    bpy.context.scene.render.resolution_x = export_profile['resolution_x']
    bpy.context.scene.render.resolution_y = export_profile['resolution_y']
    output_render_name = Path(recording_folder).name + export_profile['output_name_sufix'] + '.mp4'
    output_render_path = str(Path(recording_folder) / 'video_export' / output_render_name)
    bpy.context.scene.render.filepath = output_render_path

    # Render the animation
    bpy.ops.render.render(animation=True)

    # Restore the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    return

def create_background_nodes(
    export_profile,
    tree,
    links
) -> bpy.types.CompositorNodeScale:
    
    render_cameras_count = len(export_profile['render_cameras'])

    # Create Image node
    background_image_node = tree.nodes.new(type="CompositorNodeImage")
    background_image_node.image = bpy.data.images.load(RENDER_BACKGROUND['base_image_path'])
    background_image_node.location = (-800, (render_cameras_count + 1) * 300)
    # Color mix multiply node
    background_color_node = tree.nodes.new(type="CompositorNodeMixRGB")
    background_color_node.blend_type = 'MULTIPLY'
    background_color_node.inputs[2].default_value = RENDER_BACKGROUND['color_modifier']
    background_color_node.location = (-600, (render_cameras_count + 1) * 300)
    # Scale node
    background_scale_node = tree.nodes.new(type="CompositorNodeScale")
    background_scale_node.space = 'RENDER_SIZE'
    background_scale_node.location = (-400, (render_cameras_count + 1) * 300)

    #  Connect background nodes
    links.new(background_image_node.outputs[0], background_color_node.inputs[1])
    links.new(background_color_node.outputs[0], background_scale_node.inputs[0])

    return background_scale_node

def create_camera_nodes(
    export_profile, 
    recording_folder,
    alpha_over_nodes,
    background_end_node,
    tree,
    links
) -> None:
    
    render_cameras_count = len(export_profile['render_cameras'])

    # For each render camera create MovieClip, Scale and Translate nodes
    for index, camera in enumerate(export_profile['render_cameras']):

        #  Get a reference to the render_camera
        render_camera = export_profile['render_cameras'][camera]

        # Create a MovieClip or Render Layer node depending on the export profile
        if export_profile['prerender_cameras']:
            # Get the render camera file name
            render_camera_filename = Path(recording_folder).name + '_' + camera + '.mp4'
            render_camera_filepath = str(Path(recording_folder) / 'video_export' / 'render_cameras' / render_camera_filename)

            # Create MovieClip node
            video_node = tree.nodes.new(type="CompositorNodeMovieClip")
            video_node.clip = bpy.data.movieclips.load(render_camera_filepath)
        else:
            # Create Render Layer node
            video_node = tree.nodes.new(type="CompositorNodeRLayers")
            video_node.scene = bpy.data.scenes[f"Render_Camera_{camera}"]
        
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
        translate_node.inputs[1].default_value = export_profile['resolution_x'] * render_camera['translate_x']
        translate_node.inputs[2].default_value = export_profile['resolution_y'] * render_camera['translate_y']
        
        translate_node.location = (-400, (render_cameras_count - index) * 300)

        # Link nodes
        links.new(video_node.outputs[0], scale_node.inputs[0])
        links.new(scale_node.outputs[0], translate_node.inputs[0])

        # Create a new alpha over node
        # If alpha over nodes list is empty, connect the background and the first
        # render camera
        if not alpha_over_nodes:
            alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            alpha_over_nodes[0].location = (-200, (render_cameras_count - index) * 300)
            # Link nodes
            links.new(
                background_end_node.outputs[0],
                alpha_over_nodes[0].inputs[1]
            )
            links.new(
                translate_node.outputs[0],
                alpha_over_nodes[0].inputs[2]
            )
        else:
            # Connect the last alpha over node with the new render camera
            alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            alpha_over_nodes[-1].location = (-200, (render_cameras_count - index) * 300)
            # Link nodes
            links.new(
                alpha_over_nodes[-2].outputs[0],
                alpha_over_nodes[-1].inputs[1]
            )
            links.new(
                translate_node.outputs[0],
                alpha_over_nodes[-1].inputs[2]
            )

    return

def create_overlay_nodes(
    scene: bpy.types.Scene,
    export_profile,
    recording_folder,
    alpha_over_nodes,
    background_end_node,
    tree,
    links
):

    overlays_count = len(export_profile['overlays'])

    # For each overlay create the corresponding node
    for index, overlay in enumerate(export_profile['overlays']):

        # Get a reference to the overlay object
        overlay_dict = export_profile['overlays'][overlay]

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
        translate_node.inputs[1].default_value = export_profile['resolution_x'] * overlay_dict['translate_x']
        translate_node.inputs[2].default_value = export_profile['resolution_y'] * overlay_dict['translate_y']
        
        translate_node.location = (
            -400,
            -(overlays_count - index - 1) * 400 - 50
        )

        # Link nodes
        links.new(overlay_node.outputs[0], scale_node.inputs[0])
        links.new(scale_node.outputs[0], translate_node.inputs[0])

        # Create a new alpha over node
        # If alpha over nodes list is empty, connect the background and the first
        # overlay
        if not alpha_over_nodes:
            alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            alpha_over_nodes[0].location = (-200, -(overlays_count - index - 1) * 400 - 50)
            # Link nodes
            links.new(
                background_end_node.outputs[0],
                alpha_over_nodes[0].inputs[1]
            )
            links.new(
                translate_node.outputs[0],
                alpha_over_nodes[0].inputs[2]
            )
        else:
            # Connect the last alpha over node with the new overlay
            alpha_over_nodes.append(tree.nodes.new(type="CompositorNodeAlphaOver"))
            alpha_over_nodes[-1].location = (-200, -(overlays_count - index - 1) * 400 - 50)
            # Link nodes
            links.new(
                alpha_over_nodes[-2].outputs[0],
                alpha_over_nodes[-1].inputs[1]
            )
            links.new(
                translate_node.outputs[0],
                alpha_over_nodes[-1].inputs[2]
            )

    return
