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
    first_video_x_position = -(len(background_videos) - 1) / 2 * (videos_x_dimension + videos_x_separation)

    # Iterate through the background videos
    for video_index in range(len(background_videos)):
        
        # Set the location of the video
        background_videos[video_index].location[0] = first_video_x_position + video_index * (videos_x_dimension + videos_x_separation)