import addon_utils
import bpy
import numpy as np
from pathlib import Path
from typing import Union


def get_video_paths(path_to_video_folder: str) -> list[str]:
    """Search the folder for 'mp4' files (case insensitive) and return them as a list"""
    print(f"Searching for videos in {path_to_video_folder}")
    list_of_video_paths = list(Path(path_to_video_folder).glob("*.mp4")) + list(
        Path(path_to_video_folder).glob("*.MP4")
    )
    unique_list_of_video_paths = list(set(list_of_video_paths))
    paths_as_str = [str(path) for path in unique_list_of_video_paths]
    return paths_as_str


def add_videos_to_scene(videos_directory: str,
                        parent_object: bpy.types.Object,
                        video_scale: float = 3,
                        ):
    """Load videos for Blender 4.2 - 4.x using import_as_mesh_planes operator."""
    print(f"Adding videos to scene...")
    video_paths = get_video_paths(videos_directory)

    bpy.ops.image.import_as_mesh_planes(use_backface_culling=False,
                                        files=[{"name": path} for path in video_paths],
                                        directory=videos_directory,
                                        offset=True,
                                        size_mode='ABSOLUTE',
                                        height=video_scale,
                                        offset_amount=video_scale * .1,
                                        align_axis='+Y')
    # gather all the imported objects
    imported_objects = bpy.context.selected_objects

    # find x min/max for each video
    x_min = min([obj.location.x for obj in imported_objects])
    x_max = max([obj.location.x for obj in imported_objects])

    # center the videos
    for obj in imported_objects:
        obj.location.x -= (x_max + x_min) / 2
        obj.location.y += video_scale / 2
        obj.location.z = video_scale / 2 + 0.5

    # add to videos collection
    videos_collection = bpy.data.collections.new(name="Videos")
    bpy.context.scene.collection.children.link(videos_collection)
    for obj in imported_objects:
        videos_collection.objects.link(obj)
        obj.parent = parent_object


def add_videos_to_scene_blender_5(videos_directory: str,
                                  parent_object: bpy.types.Object,
                                  video_scale: float = 3,
                                  ):
    """
    Load videos into scene using Blender 5+ Mesh Plane operator.

    In Blender 5+, the 'Import Images as Planes' addon was replaced with
    a built-in 'Mesh Plane' operator accessible via Add -> Image -> Mesh Plane.

    This function tries multiple operator names and fallback methods.
    """
    print(f"Adding videos to scene (Blender 5+ method)...")
    video_paths = get_video_paths(videos_directory)

    imported_objects = []

    # Try to find the correct operator for Blender 5+
    # Check available operators
    mesh_ops = [op for op in dir(bpy.ops.mesh) if not op.startswith('_')]
    object_ops = [op for op in dir(bpy.ops.object) if not op.startswith('_')]
    image_ops = [op for op in dir(bpy.ops.image) if not op.startswith('_')]

    print(
        f"Available mesh operators with 'import' or 'plane': {[o for o in mesh_ops if 'import' in o or 'plane' in o]}")
    print(f"Available object operators with 'import': {[o for o in object_ops if 'import' in o]}")
    print(f"Available image operators: {image_ops}")

    for video_path in video_paths:
        video_name = Path(video_path).name
        print(f"Importing: {video_name}")

        success = False

        # Method 1: Try import_mesh_plane under different namespaces
        for op_path in ['bpy.ops.mesh.import_image_as_plane',
                        'bpy.ops.object.import_image_as_plane',
                        'bpy.ops.image.import_as_mesh_planes']:
            try:
                parts = op_path.split('.')
                module = getattr(bpy.ops, parts[1])
                operator = getattr(module, parts[2])
                operator(
                    filepath=str(video_path),
                    relative_path=True,
                )
                if bpy.context.selected_objects:
                    imported_objects.extend(bpy.context.selected_objects)
                    success = True
                    print(f"  Success with {op_path}")
                    break
            except (AttributeError, TypeError) as e:
                continue

        # Method 2: Use the import_as_mesh_planes operator (works in Blender 5.1!)
        if not success:
            try:
                # Use size_mode='ABSOLUTE' to maintain aspect ratio while setting height
                bpy.ops.image.import_as_mesh_planes(
                    files=[{"name": video_name}],
                    directory=str(Path(video_path).parent),
                    shader='EMISSION',
                    align_axis='+Y',
                    size_mode='ABSOLUTE',
                    height=video_scale,
                )
                if bpy.context.selected_objects:
                    imported_objects.extend(bpy.context.selected_objects)
                    success = True
                    print(f"  Success with import_as_mesh_planes")
            except (AttributeError, TypeError) as e:
                print(f"  import_as_mesh_planes failed: {e}")

        # Method 3: Fallback - create plane manually with image texture
        if not success:
            try:
                print(f"  Using fallback method (manual plane + texture)...")

                # Create plane
                bpy.ops.mesh.primitive_plane_add(
                    size=video_scale,
                    location=(0, 0, 0),
                    rotation=(np.pi / 2, 0, 0)  # Rotate to face -Y like other videos
                )
                plane = bpy.context.active_object
                plane.name = f"video_{video_name}"

                # Load image
                try:
                    img = bpy.data.images.load(filepath=str(video_path), check_existing=True)
                except Exception as img_e:
                    print(f"    Could not load image: {img_e}")
                    img = None

                if img:
                    # Create material with image texture
                    mat = bpy.data.materials.new(name=f"mat_{video_name}")
                    mat.use_nodes = True
                    nodes = mat.node_tree.nodes
                    links = mat.node_tree.links

                    # Get or create output node
                    output_node = None
                    for node in nodes:
                        if node.type == 'OUTPUT_MATERIAL':
                            output_node = node
                            break
                    if not output_node:
                        output_node = nodes.new('ShaderNodeOutputMaterial')

                    # Create Principled BSDF
                    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')

                    # Create image texture node
                    tex_node = nodes.new('ShaderNodeTexImage')
                    tex_node.image = img

                    # Link texture to base color
                    links.new(tex_node.outputs['Color'], bsdf_node.inputs['Base Color'])
                    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

                    # Assign material to plane
                    if plane.data.materials:
                        plane.data.materials[0] = mat
                    else:
                        plane.data.materials.append(mat)

                imported_objects.append(plane)
                success = True
                print(f"  Success with fallback method")

            except Exception as fallback_e:
                print(f"  Fallback method failed: {fallback_e}")

    # Offset the videos horizontally
    # Note: import_as_mesh_planes with align_axis='+Y' handles rotation automatically
    if imported_objects:
        buffer = video_scale * 1.1
        for i, obj in enumerate(imported_objects):
            x_offset = (i - (len(imported_objects) - 1) / 2) * buffer
            obj.location.x = x_offset
            obj.location.y = video_scale / 2
            obj.location.z = video_scale / 2 + 0.5

    # Create videos collection
    videos_collection = bpy.data.collections.new(name="Videos")
    bpy.context.scene.collection.children.link(videos_collection)
    for obj in imported_objects:
        # Unlink from current collection first if needed
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        videos_collection.objects.link(obj)
        obj.parent = parent_object

    print(f"Successfully imported {len(imported_objects)} videos using Blender 5+ method")


def add_videos_to_scene_pre_4_2(videos_path: Union[Path, str],
                                parent_object: bpy.types.Object,
                                video_location_scale: float = 4,
                                video_size_scale: float = 5,
                                ):
    """Load videos for Blender versions before 4.2 using the old import_image.to_plane operator."""
    print(f"Adding videos to scene...")

    number_of_videos = len(list(get_video_paths(videos_path)))
    print(f"Found {number_of_videos} videos in {videos_path}")
    for (
            video_number,
            video_path,
    ) in enumerate(get_video_paths(videos_path)):
        print(f"Adding video: {Path(video_path).name} to scene")

        bpy.ops.import_image.to_plane(
            files=[{"name": Path(video_path).name}],
            directory=str(Path(video_path).parent),
            shader="EMISSION",
        )
        print(f"Added video: {Path(video_path).name} to scene")
        video_as_plane = bpy.context.editable_objects[-1]
        print(f"video_as_plane: {video_as_plane}")
        video_as_plane.name = "video_" + str(video_number)
        print(f"video_as_plane.name: {video_as_plane.name}")
        buffer = 1.1
        vid_x = (video_number * buffer - np.mean(np.arange(0, number_of_videos))) * video_location_scale

        video_as_plane.location = [
            vid_x,
            video_location_scale,
            video_size_scale * .6
        ]
        video_as_plane.rotation_euler = [np.pi / 2, 0, 0]
        video_as_plane.scale = [video_size_scale] * 3
        video_as_plane.parent = parent_object


def load_videos_as_planes(recording_path: str,
                          parent_object: bpy.types.Object = None, ):
    """
    ############################
    Load videos into scene using appropriate method based on Blender version.

    Version handling:
    - Blender 5.0+: Uses new built-in Mesh Plane operator (bpy.ops.image.import_mesh_plane)
    - Blender 4.2 - 4.x: Uses io_import_images_as_planes addon (bpy.ops.image.import_as_mesh_planes)
    - Blender < 4.2: Uses old import_image.to_plane operator
    """
    recording_path = Path(recording_path)

    if Path(recording_path / "annotated_videos").is_dir():
        videos_path = Path(recording_path / "annotated_videos")
    elif Path(recording_path / "synchronized_videos").is_dir():
        videos_path = Path(recording_path / "synchronized_videos")
    else:
        print("Did not find an `annotated_videos` or `synchronized_videos` folder in the recording path")
        videos_path = None

    if videos_path is not None:
        blender_version = bpy.app.version
        print(f"Blender version: {blender_version}")

        try:
            # Blender 5.0+ uses built-in Mesh Plane (no addon needed)
            if blender_version[0] >= 5:
                print("Using Blender 5+ Mesh Plane import method")
                add_videos_to_scene_blender_5(
                    videos_directory=str(videos_path),
                    parent_object=parent_object
                )
            # Blender 4.2 - 4.x uses import_as_mesh_planes from addon
            elif blender_version[0] >= 4 and blender_version[1] >= 2:
                print("Using Blender 4.2+ import_as_mesh_planes method")
                try:
                    addon_utils.enable("io_import_images_as_planes")
                except Exception as e:
                    print("Warning: Could not enable io_import_images_as_planes addon: ")
                    print(e)
                add_videos_to_scene(
                    videos_directory=str(videos_path),
                    parent_object=parent_object
                )
            # Blender < 4.2 uses old import_image.to_plane
            else:
                print("Using pre-4.2 import_image.to_plane method")
                try:
                    addon_utils.enable("io_import_images_as_planes")
                except Exception as e:
                    print("Warning: Could not enable io_import_images_as_planes addon: ")
                    print(e)
                add_videos_to_scene_pre_4_2(
                    videos_path=str(videos_path),
                    parent_object=parent_object
                )

        except Exception as e:
            print("Error adding videos to scene: ")
            print(e)
