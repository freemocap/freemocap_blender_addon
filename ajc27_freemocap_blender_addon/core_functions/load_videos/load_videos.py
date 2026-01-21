"""
Load videos as planes for Blender 3.x, 4.x, and 5.x

Compatibility:
- Blender 3.0 - 4.1: Uses `io_import_images_as_planes` addon with `bpy.ops.import_image.to_plane()`
- Blender 4.2+: Uses built-in `bpy.ops.image.import_as_mesh_planes()` (no addon required)
"""

import addon_utils
import bpy
import numpy as np
from pathlib import Path


# =============================================================================
# Version Detection
# =============================================================================

def _blender_version_at_least(major: int, minor: int) -> bool:
    """
    Check if Blender version is at least major.minor using proper tuple comparison.
    
    This correctly handles cases like:
    - (5, 0) >= (4, 2) -> True  (Blender 5.0)
    - (4, 2) >= (4, 2) -> True  (Blender 4.2)
    - (4, 1) >= (4, 2) -> False (Blender 4.1)
    """
    return bpy.app.version[:2] >= (major, minor)


def _has_builtin_mesh_planes_operator() -> bool:
    """Check if the built-in import_as_mesh_planes operator exists (Blender 4.2+)."""
    return hasattr(bpy.ops.image, "import_as_mesh_planes")


def _has_addon_to_plane_operator() -> bool:
    """Check if the addon-based to_plane operator exists (Blender 3.x - 4.1)."""
    return hasattr(bpy.ops.import_image, "to_plane")


def _get_import_method() -> str:
    """
    Determine which import method to use based on version and available operators.
    
    Returns:
        "builtin" for Blender 4.2+
        "addon" for Blender 3.x - 4.1
        
    Raises:
        RuntimeError if no suitable import method is available.
    """
    # Primary check: version-based
    if _blender_version_at_least(4, 2):
        # Verify the operator actually exists
        if _has_builtin_mesh_planes_operator():
            return "builtin"
        raise RuntimeError(
            f"Blender {bpy.app.version_string} should have built-in image.import_as_mesh_planes "
            "but it was not found. This is unexpected."
        )
    
    # Fallback for older versions: use addon
    return "addon"


# =============================================================================
# Video Path Discovery
# =============================================================================

def get_video_paths(path_to_video_folder: str) -> list[str]:
    """
    Search the folder for video files (mp4, case insensitive) and return them as a list.
    
    Args:
        path_to_video_folder: Path to the folder containing videos.
        
    Returns:
        List of absolute paths to video files as strings.
    """
    print(f"Searching for videos in {path_to_video_folder}")
    folder = Path(path_to_video_folder)
    
    # Collect both .mp4 and .MP4 (and any other case variations on case-sensitive systems)
    video_paths = list(folder.glob("*.mp4")) + list(folder.glob("*.MP4"))
    
    # Deduplicate (in case of case-insensitive filesystem)
    unique_paths = list(set(video_paths))
    
    # Sort for consistent ordering
    unique_paths.sort(key=lambda p: p.name.lower())
    
    paths_as_str = [str(path) for path in unique_paths]
    print(f"Found {len(paths_as_str)} videos")
    return paths_as_str


# =============================================================================
# Blender 4.2+ Import (Built-in)
# =============================================================================

def _add_videos_builtin(
    videos_directory: str,
    parent_object: bpy.types.Object | None,
    video_scale: float,
) -> None:
    """
    Add videos using Blender 4.2+ built-in import_as_mesh_planes operator.
    
    Args:
        videos_directory: Path to directory containing video files.
        parent_object: Optional parent object for the imported planes.
        video_scale: Height of the video planes in Blender units.
    """
    print(f"Using Blender {bpy.app.version_string} built-in mesh planes import")
    
    video_paths = get_video_paths(videos_directory)
    if not video_paths:
        print("No videos found to add.")
        return
    
    # The built-in operator expects files as a list of dicts with "name" keys
    # containing just the filename, not the full path
    files_list = [{"name": Path(path).name} for path in video_paths]
    
    bpy.ops.image.import_as_mesh_planes(
        files=files_list,
        directory=videos_directory,
        use_backface_culling=False,
        offset=True,
        height=video_scale,
        offset_amount=video_scale * 0.1,
        align_axis='-Y',
        shader='EMISSION',
    )
    
    _post_process_imported_planes(parent_object=parent_object, video_scale=video_scale)


# =============================================================================
# Blender 3.x - 4.1 Import (Addon-based)
# =============================================================================

def _enable_images_as_planes_addon() -> None:
    """
    Enable the io_import_images_as_planes addon required for Blender < 4.2.
    
    Raises:
        RuntimeError if the addon cannot be enabled.
    """
    addon_name = "io_import_images_as_planes"
    
    # Check if already enabled
    if addon_name in {mod.module for mod in bpy.context.preferences.addons}:
        print(f"Addon '{addon_name}' is already enabled")
        return
    
    try:
        addon_utils.enable(addon_name)
        print(f"Enabled addon: {addon_name}")
    except Exception as e:
        raise RuntimeError(
            f"Failed to enable '{addon_name}' addon required for Blender {bpy.app.version_string}. "
            f"Error: {e}"
        ) from e
    
    # Verify the operator is now available
    if not _has_addon_to_plane_operator():
        raise RuntimeError(
            f"Addon '{addon_name}' was enabled but bpy.ops.import_image.to_plane is not available."
        )


def _add_videos_addon(
    videos_directory: str,
    parent_object: bpy.types.Object | None,
    video_location_scale: float,
    video_size_scale: float,
) -> None:
    """
    Add videos using the io_import_images_as_planes addon (Blender 3.x - 4.1).
    
    Args:
        videos_directory: Path to directory containing video files.
        parent_object: Optional parent object for the imported planes.
        video_location_scale: Spacing multiplier for video positions.
        video_size_scale: Scale factor for video plane size.
    """
    print(f"Using Blender {bpy.app.version_string} addon-based import")
    
    _enable_images_as_planes_addon()
    
    video_paths = get_video_paths(videos_directory)
    if not video_paths:
        print("No videos found to add.")
        return
    
    number_of_videos = len(video_paths)
    
    for video_number, video_path in enumerate(video_paths):
        video_path = Path(video_path)
        print(f"Adding video {video_number + 1}/{number_of_videos}: {video_path.name}")
        
        bpy.ops.import_image.to_plane(
            files=[{"name": video_path.name}],
            directory=str(video_path.parent),
            shader="EMISSION",
        )
        
        video_as_plane = bpy.context.editable_objects[-1]
        video_as_plane.name = f"video_{video_number}"
        
        # Calculate position to center videos horizontally
        buffer = 1.1
        vid_x = (video_number * buffer - np.mean(np.arange(0, number_of_videos))) * video_location_scale
        
        video_as_plane.location = [
            vid_x,
            video_location_scale,
            video_size_scale * 0.6,
        ]
        video_as_plane.rotation_euler = [np.pi / 2, 0, 0]
        video_as_plane.scale = [video_size_scale] * 3
        
        if parent_object is not None:
            video_as_plane.parent = parent_object
        
        print(f"Added: {video_as_plane.name}")


# =============================================================================
# Post-Processing (Blender 4.2+)
# =============================================================================

def _post_process_imported_planes(
    parent_object: bpy.types.Object | None,
    video_scale: float,
) -> None:
    """
    Post-process planes imported by the built-in operator (Blender 4.2+).
    Centers them and optionally parents them.
    
    Args:
        parent_object: Optional parent object for the imported planes.
        video_scale: Height of the video planes in Blender units.
    """
    imported_objects = bpy.context.selected_objects
    
    if not imported_objects:
        print("Warning: No objects were imported.")
        return
    
    print(f"Post-processing {len(imported_objects)} imported plane(s)")
    
    # Find x extent for centering
    x_min = min(obj.location.x for obj in imported_objects)
    x_max = max(obj.location.x for obj in imported_objects)
    x_center = (x_max + x_min) / 2
    
    # Center and position the videos
    for obj in imported_objects:
        obj.location.x -= x_center
        obj.location.y += video_scale / 2
        obj.location.z = video_scale / 2 + 0.5
    
    # Create a collection for the videos
    videos_collection = bpy.data.collections.new(name="Videos")
    bpy.context.scene.collection.children.link(videos_collection)
    
    for obj in imported_objects:
        # Link to Videos collection
        videos_collection.objects.link(obj)
        
        # Set parent
        if parent_object is not None:
            obj.parent = parent_object


# =============================================================================
# Main Entry Point
# =============================================================================

def load_videos_as_planes(
    recording_path: str,
    parent_object: bpy.types.Object | None = None,
) -> None:
    """
    Load videos into scene using the appropriate method for the Blender version.
    
    Automatically detects:
    - Blender 4.2+ (including 5.x): Uses built-in bpy.ops.image.import_as_mesh_planes
    - Blender 3.x - 4.1: Uses io_import_images_as_planes addon
    
    Args:
        recording_path: Path to the recording directory containing video folders.
        parent_object: Optional parent object for the imported video planes.
    """
    print(f"\n{'='*60}")
    print(f"Loading videos as planes (Blender {bpy.app.version_string})")
    print(f"{'='*60}")
    
    recording_path = Path(recording_path)
    
    # Find video directory
    annotated_path = recording_path / "annotated_videos"
    synchronized_path = recording_path / "synchronized_videos"
    
    if annotated_path.is_dir():
        videos_path = annotated_path
    elif synchronized_path.is_dir():
        videos_path = synchronized_path
    else:
        print(
            f"Warning: Did not find 'annotated_videos' or 'synchronized_videos' folder "
            f"in {recording_path}"
        )
        return
    
    print(f"Video directory: {videos_path}")
    
    # Determine and use the appropriate import method
    import_method = _get_import_method()
    
    if import_method == "builtin":
        _add_videos_builtin(
            videos_directory=str(videos_path),
            parent_object=parent_object,
            video_scale=3.0,
        )
    elif import_method == "addon":
        _add_videos_addon(
            videos_directory=str(videos_path),
            parent_object=parent_object,
            video_location_scale=4.0,
            video_size_scale=5.0,
        )
    else:
        raise RuntimeError(f"Unknown import method: {import_method}")
    
    print(f"{'='*60}")
    print("Video loading complete")
    print(f"{'='*60}\n")