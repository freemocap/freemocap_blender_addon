import bpy
import os
import math
from mathutils import Matrix, Quaternion

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None
    try:
        import toml
    except ModuleNotFoundError:
        toml = None

# Assumed fixed sensor width in mm becuase the variable is the focal length
DEFAULT_SENSOR_WIDTH = 36.0 # Same as Blender default

def add_capture_cameras(
    recording_folder: str='',
) -> None:
    calibration_file_path = None

    # Find the calibration file in the recording folder
    for file in os.listdir(recording_folder):
        if file.endswith('.toml'):
            calibration_file_path = os.path.join(recording_folder, file)
    
    # If there is no calibration file, return
    if calibration_file_path is None:
        print('No calibration file found in the recording folder')
        return

    # Load the TOML file
    if tomllib is not None:
        with open(calibration_file_path, 'rb') as file:
            data = tomllib.load(file)
    else:
        with open(calibration_file_path, 'r') as file:
            data = toml.load(file)

    # Check if the groundplane_calibration variable exists and is true
    if 'groundplane_calibration' not in data['metadata'].keys():
        print('Groundplane calibration is not enabled')
        return
    
    if not data['metadata']['groundplane_calibration']:
        print('Groundplane calibration is not enabled')
        return

    # Extract camera information into a dictionary
    cameras_dict = {}
    for key, value in data.items():
        if key.startswith('cam_'):
            cameras_dict[key] = value

    # Find the data origin empty object to parent the cameras
    for obj in bpy.data.objects:
        # If the object name end with '_origin', it is the data origin
        if obj.name.endswith('_origin'):
            data_origin = obj
            break

    # Create a new empty object to parent the cameras
    bpy.ops.object.empty_add(
        type='ARROWS',
        align='WORLD',
        location=(0, 0, 0),
        scale=(0.1, 0.1, 0.1)
    )
    cameras_parent = bpy.context.active_object
    cameras_parent.name = 'capture_cameras_parent'
    cameras_parent.parent = data_origin
    # Hide the camera parent in viewport
    cameras_parent.hide_set(True)

    # Set the scene resolution equal to cam_0 resolution
    bpy.context.scene.render.resolution_x = cameras_dict['cam_0']['size'][0]
    bpy.context.scene.render.resolution_y = cameras_dict['cam_0']['size'][1]

    # TODO: Change the synchronized videos for annotated videos when those
    # they are not being used elsewhere to avoid EXCEPTION_ACCESS_VIOLATION

    # Get a list of the videos in the synchronized videos folder
    # This is because the calibration and capture can be in different folders
    # So in the calibration file there is no link between the calibration camera videos
    # and the final capture videos
    synchronized_videos_folder = os.path.join(recording_folder, 'synchronized_videos')
    synchronized_videos = [f for f in os.listdir(synchronized_videos_folder) if f.endswith('.mp4')]

    # Add the cameras to the scene
    for key, camera_data in cameras_dict.items():

        bpy.ops.object.camera_add(
            location=[coord / 1000 for coord in camera_data['world_position']]
        )

        camera_object = bpy.context.object

        # Rotate the camera
        rotation_matrix = Matrix(camera_data['world_orientation'])
        rotation_quaternion = rotation_matrix.to_quaternion()
        
        rotation_flip = Quaternion((1.0, 0.0, 0.0), math.pi) # 180° around X

        rotation_quaternion_fixed = rotation_quaternion @ rotation_flip

        camera_object.rotation_mode = 'QUATERNION'
        camera_object.rotation_quaternion = rotation_quaternion_fixed

        # Intrinsics
        fx = camera_data['matrix'][0][0]  # focal length in px along x
        width_px, height_px = camera_data['size']

        # Set sensor size
        camera_object.data.sensor_width = DEFAULT_SENSOR_WIDTH

        # Convert focal length from px → mm. Using max(width_px, height_px)
        # to use landscape or portrait camera orientations.
        # Not a robust solution according to AI but the only thing that worked 
        f_mm = fx * (camera_object.data.sensor_width / max(width_px, height_px))

        camera_object.data.lens_unit = 'MILLIMETERS'
        camera_object.data.lens = f_mm

        # Set the name of the camera
        camera_object.name = 'Capture_' + key
        # Show the name in the viewport
        camera_object.show_name = True
        # Reduce the scale of the camera object
        camera_object.scale = (0.3, 0.3, 0.3)

        # Parent the camera to the cameras parent
        camera_object.parent = cameras_parent

        # Add the correspondent capture video to the background of each camera
        # Get the path of the capture video
        capture_video_path = (
            recording_folder
            + '/synchronized_videos/'
            + synchronized_videos[int(key.split('_')[1])]
        )

        # Normalize the path
        capture_video_path = os.path.normpath(capture_video_path)

        # Load the capture video
        capture_video = bpy.data.movieclips.load(capture_video_path)

        # Add the capture video as a background image
        camera_data = camera_object.data
        camera_background = camera_data.background_images.new()
        camera_background.source = 'MOVIE_CLIP'
        camera_background.clip = capture_video
        camera_background.alpha = 1
        camera_background.clip.frame_offset = 1
        camera_data.show_background_images = True

    return
