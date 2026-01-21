"""
Rearrange background video planes in Blender.

Compatible with Blender 3.x, 4.x, and 5.x.
"""

import bpy


def rearrange_background_videos(
    scene: bpy.types.Scene,
    videos_x_separation: float = 0.1,
) -> None:
    """
    Rearrange background video planes to be evenly spaced and horizontally centered.
    
    Finds all objects in the scene whose name contains 'video_' and repositions
    them along the X axis with the specified separation.
    
    Args:
        scene: The Blender scene containing the video objects.
        videos_x_separation: Gap between video planes in Blender units.
        
    Raises:
        ValueError: If no background videos are found in the scene.
    """
    # Find all video objects
    background_videos = [obj for obj in scene.objects if 'video_' in obj.name]
    
    if not background_videos:
        raise ValueError(
            f"No background videos found in scene '{scene.name}'. "
            "Expected objects with 'video_' in their name."
        )
    
    # Sort by name for consistent ordering
    background_videos.sort(key=lambda obj: obj.name)
    
    num_videos = len(background_videos)
    print(f"Rearranging {num_videos} background video(s)")
    
    # Get the x dimension from the first video (assume all are the same size)
    videos_x_dimension = background_videos[0].dimensions.x
    
    # Calculate total width and starting position
    # Videos are positioned so their centers are evenly spaced
    total_span = (num_videos - 1) * (videos_x_dimension + videos_x_separation)
    first_video_x_position = -total_span / 2
    
    # Position each video
    for video_index, video in enumerate(background_videos):
        new_x = first_video_x_position + video_index * (videos_x_dimension + videos_x_separation)
        video.location.x = new_x
        print(f"  {video.name}: x = {new_x:.3f}")
    
    print("Background videos rearranged successfully")