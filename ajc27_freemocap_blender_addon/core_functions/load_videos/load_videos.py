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
    print(f"Adding videos to scene...")
    video_paths = get_video_paths(videos_directory)

    bpy.ops.image.import_as_mesh_planes(use_backface_culling=False,
                                        files=[{"name":path} for path in video_paths],
                                        directory=videos_directory,
                                        offset=True,
                                        height=video_scale,
                                        offset_amount= video_scale*.1,
                                        align_axis='-Y')
    # gather all the imported objects
    imported_objects = bpy.context.selected_objects

    #find x min/max for each video
    x_min = min([obj.location.x for obj in imported_objects])
    x_max = max([obj.location.x for obj in imported_objects])


    #center the videos
    for obj in imported_objects:
        obj.location.x -= (x_max + x_min) / 2
        obj.location.y += video_scale/2
        obj.location.z = video_scale/2 + 0.5




    #add to videos collection
    videos_collection = bpy.data.collections.new(name="Videos")
    bpy.context.scene.collection.children.link(videos_collection)
    for obj in imported_objects:
        videos_collection.objects.link(obj)
        obj.parent = parent_object



def add_videos_to_scene_pre_4_2(videos_path: Union[Path, str],
                                parent_object: bpy.types.Object,
                                video_location_scale: float = 4,
                                video_size_scale: float = 5,
                                ):
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
    Load videos into scene using `videos_as_planes` addon
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
        try:
            addon_utils.enable("io_import_images_as_planes")
        except Exception as e:
            print("Error enabling `io_import_images_as_planes` addon: ")
            print(e)
        try:
            if bpy.app.version[0] >= 4 and bpy.app.version[1] >= 2:
                add_videos_to_scene(videos_directory=str(videos_path), parent_object=parent_object)
            else:
                add_videos_to_scene_pre_4_2(videos_path=str(videos_path), parent_object=parent_object)

        except Exception as e:
            print("Error adding videos to scene: ")
            print(e)
