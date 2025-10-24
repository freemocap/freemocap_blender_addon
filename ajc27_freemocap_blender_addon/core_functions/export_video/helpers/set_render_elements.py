import bpy
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES
)

def set_render_elements(
    scene: bpy.types.Scene,
    export_profile: dict,
) -> None:
    
    def set_hide_render_recursive(obj):
        obj.hide_render = False
        for child in obj.children:
            set_hide_render_recursive(child)

    # If the render_elements list is empty, fill it with the visible objects in the scene
    if export_profile['render_elements'] == []:
        if scene.freemocap_ui_properties.show_skelly_mesh:
            export_profile['render_elements'].append('skelly_mesh')
        if scene.freemocap_ui_properties.show_rigid_bodies:
            export_profile['render_elements'].append('rigid_body_meshes')
        if scene.freemocap_ui_properties.show_center_of_mass:
            export_profile['render_elements'].append('center_of_mass')
        if scene.freemocap_ui_properties.show_videos:
            export_profile['render_elements'].append('videos')
        if scene.freemocap_ui_properties.show_joint_angles:
            export_profile['render_elements'].append('joint_angles')
        if scene.freemocap_ui_properties.show_base_of_support:
            export_profile['render_elements'].append('base_of_support')

    else:
        print("Using existing render elements: " + str(export_profile['render_elements']))

    # Set hide_render equal to True for all the objects excepts cameras and lights
    for obj in bpy.data.objects:
        if obj.type not in ['CAMERA', 'LIGHT']:
            obj.hide_render = True

    # Set hide_render equal to False for the render elements
    for obj in bpy.data.objects:
        # if any(element in obj.name for element in EXPORT_PROFILES[export_profile]['render_elements']):
        if any(element in obj.name for element in export_profile['render_elements']):
            print("Unhiding for render: " + obj.name)
            set_hide_render_recursive(obj)

    return
