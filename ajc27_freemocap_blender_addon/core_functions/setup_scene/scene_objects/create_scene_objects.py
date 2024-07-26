import bpy


def create_scene_objects(scene: bpy.types.Scene, export_profile: str = 'debug') -> None:
    from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.ground_plane.create_ground_plane import \
        create_ground_plane
    from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.lights.create_lights import create_lights

    # from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.cameras.create_cameras import create_cameras
    # cameras = create_cameras(scene=scene, export_profile=export_profile)
    create_lights(scene=scene, cameras_positions=cameras)
    create_ground_plane()

    # Place the required cameras
    cameras_positions = create_cameras(scene, export_profile)

    # Place the required lights
    create_lights(scene, cameras_positions)



if __name__ == "__main__":
    print('hiiii')
    create_scene_objects(bpy.context.scene, export_profile='debug')
