import bpy



def create_scene_objects(scene: bpy.types.Scene, export_profile: str = 'debug') -> None:
    create_cameras = None
    create_ground_plane = None
    create_lights = None

    try:
        from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.cameras.create_cameras import \
            create_cameras
    except Exception as exc:
        print(f"Failed to import create_cameras: {exc}")

    try:
        from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.ground_plane.create_ground_plane import \
            create_ground_plane
    except Exception as exc:
        print(f"Failed to import create_ground_plane: {exc}")

    try:
        from ajc27_freemocap_blender_addon.core_functions.setup_scene.scene_objects.lights.create_lights import \
            create_lights
    except Exception as exc:
        print(f"Failed to import create_lights: {exc}")

    cameras_positions = None

    if create_cameras is not None:
        try:
            cameras_positions = create_cameras(scene, export_profile)
        except Exception as exc:
            print(f"Failed to create cameras: {exc}")

    if create_ground_plane is not None:
        try:
            create_ground_plane()
        except Exception as exc:
            print(f"Failed to create ground plane: {exc}")

    if create_lights is not None:
        if cameras_positions:
            try:
                create_lights(scene, cameras_positions)
            except Exception as exc:
                print(f"Failed to create lights: {exc}")
        else:
            print("Skipping lights creation: no camera positions available.")



if __name__ == "__main__":
    print('hiiii')
    create_scene_objects(bpy.context.scene, export_profile='debug')
