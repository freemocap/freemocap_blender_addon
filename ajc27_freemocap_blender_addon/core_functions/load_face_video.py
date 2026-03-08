import addon_utils
import bpy
import math
from pathlib import Path

def get_video_paths(path_to_video_folder: str) -> list[str]:
    """Search the folder for 'mp4' files (case insensitive) and return them as a list"""
    list_of_video_paths = list(Path(path_to_video_folder).glob("*.mp4")) + list(
        Path(path_to_video_folder).glob("*.MP4")
    )
    unique_list_of_video_paths = list(set(list_of_video_paths))
    paths_as_str = [str(path) for path in unique_list_of_video_paths]
    return paths_as_str

def add_face_video_to_scene(
    videos_directory: str,
    parent_object: bpy.types.Object,
    video_scale: float = 0.4,
    frame_offset: int = 1,
    video_location_offset: list[float] = [0.3, 0, 0]
    ):
    video_paths = get_video_paths(videos_directory)
    if not video_paths:
        print(f"No face video found in {videos_directory}")
        return

    # In Blender 4.2+, import_as_mesh_planes imports all files passed in the list 
    bpy.ops.image.import_as_mesh_planes(use_backface_culling=False,
                                        files=[{"name": path} for path in video_paths],
                                        directory=videos_directory,
                                        offset=True,
                                        height=video_scale,
                                        align_axis='-Y')
    
    imported_objects = bpy.context.selected_objects
    for obj in imported_objects:
        obj.parent = parent_object
        
        # Position the video plane
        # Ensure parent inverse is identity so location behaves relative to parent
        obj.matrix_parent_inverse.identity()
        obj.location = video_location_offset
        obj.rotation_euler = (math.pi / 2, 0, 0)

        # Apply frame offset to the video texture
        for material_slot in obj.material_slots:
            if material_slot.material and material_slot.material.use_nodes:
                nodes = material_slot.material.node_tree.nodes
                for node in nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        # Offset the video playback by adjusting the frame
                        node.image_user.frame_offset = frame_offset

def add_face_video_to_scene_pre_4_2(
    videos_path: str,
    parent_object: bpy.types.Object,
    video_scale: float = 0.4,
    frame_offset: int = 1,
    video_location_offset: list[float] = [0.3, 0, 0]
    ):
    video_paths = get_video_paths(videos_path)
    if not video_paths:
        print(f"No face video found in {videos_path}")
        return

    for video_number, video_path in enumerate(video_paths):
        bpy.ops.import_image.to_plane(
            files=[{"name": Path(video_path).name}],
            directory=str(Path(video_path).parent),
            shader="EMISSION",
        )
        
        video_as_plane = bpy.context.editable_objects[-1]
        video_as_plane.name = f"face_video_{video_number}"
        
        video_as_plane.parent = parent_object
        video_as_plane.matrix_parent_inverse.identity()
        video_as_plane.location = video_location_offset
        video_as_plane.rotation_euler = (math.pi / 2, 0, 0)
        video_as_plane.scale = (video_scale, video_scale, video_scale)

        # Apply frame offset to the video texture
        for material_slot in video_as_plane.material_slots:
            if material_slot.material and material_slot.material.use_nodes:
                nodes = material_slot.material.node_tree.nodes
                for node in nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        # Offset the video playback by adjusting the frame
                        node.image_user.frame_offset = frame_offset

def load_face_video(
    recording_folder: str,
    data_parent_name: str,
    video_scale: float = 0.4,
    move_video_with_head: bool = True,
    video_location_offset: list[float] = [0.3, 0, 0]
    ):

    recording_folder_path = Path(recording_folder)
    face_blendshapes_dir = recording_folder_path / "output_data" / "face_blendshapes"
    
    if not face_blendshapes_dir.exists():
        print(f"Face blendshapes folder not found at {face_blendshapes_dir}")
        return
        
    data_parent = bpy.data.objects.get(data_parent_name)
    if not data_parent:
        print(f"Warning: data_parent '{data_parent_name}' not found!")
        return

    # 1. Find the armature in the data parent hierarchy
    armature = None
    for child in data_parent.children_recursive:
        if child.type == 'ARMATURE':
            armature = child
            break
            
    if not armature:
        print("Warning: Armature not found for face video parenting.")
        return

    if "face" not in armature.pose.bones:
        print("Warning: 'face' bone not found in the armature.")
        return

    # 2. Setup the face_video_parent empty with constraints
    empty_name = "face_video_parent"
    if empty_name not in bpy.data.objects:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        empty = bpy.context.active_object
        empty.name = empty_name
        empty.empty_display_size = 0.1
    else:
        empty = bpy.data.objects[empty_name]
        
    # Parent the empty to the data_parent_name
    empty.parent = data_parent
    # Hide the empty
    empty.hide_set(True)

    if move_video_with_head:
        # Copy Location
        loc_con = empty.constraints.get('Copy Location') or empty.constraints.new(type='COPY_LOCATION')
        loc_con.name = 'Copy Location'
        loc_con.target = armature
        loc_con.subtarget = "face"
        loc_con.target_space = 'WORLD'
        loc_con.owner_space = 'WORLD'
    
        # Copy Rotation on Global Z
        rot_con = empty.constraints.get('Copy Rotation') or empty.constraints.new(type='COPY_ROTATION')
        rot_con.name = 'Copy Rotation'
        rot_con.target = armature
        rot_con.subtarget = "face"
        rot_con.use_x = False
        rot_con.use_y = False
        rot_con.use_z = True
        rot_con.target_space = 'WORLD'
        rot_con.owner_space = 'WORLD'

    else:
        empty.location = (0.5, 0, 1.5)
        video_location_offset = [0, 0, 0]

    # 3. Import the videos as planes
    try:
        addon_utils.enable("io_import_images_as_planes")
    except Exception as e:
        print("Error enabling `io_import_images_as_planes` addon: ", e)
        
    try:
        if bpy.app.version[0] >= 4 and bpy.app.version[1] >= 2:
            add_face_video_to_scene(
                videos_directory=str(face_blendshapes_dir), 
                parent_object=empty,
                video_scale=video_scale,
                video_location_offset=video_location_offset
            )
        else:
            add_face_video_to_scene_pre_4_2(
                videos_path=str(face_blendshapes_dir), 
                parent_object=empty,
                video_scale=video_scale,
                video_location_offset=video_location_offset
            )
    except Exception as e:
        print("Error adding face video to scene: ", e)
