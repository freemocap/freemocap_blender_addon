import bpy


def create_scene_objects(scene: bpy.types.Scene, export_profile: str = 'debug') -> None:
    from freemocap_blender_addon.core_functions.setup_scene.scene_objects.create_ground_plane import \
        create_ground_plane
    from freemocap_blender_addon.core_functions.setup_scene.scene_objects.create_lights import create_lights

    from freemocap_blender_addon.core_functions.setup_scene.scene_objects.create_render_cameras import create_cameras_objects
    
    # Place the required cameras
    cameras_positions = create_cameras_objects(scene, export_profile)

    # Place the required lights
    create_lights(scene, cameras_positions)

    create_ground_plane()


if __name__ == "__main__":
    print('hiiii')
    create_scene_objects(bpy.context.scene, export_profile='debug')
