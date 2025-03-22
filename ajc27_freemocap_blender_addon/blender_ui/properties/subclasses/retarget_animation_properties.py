import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

def get_available_armatures(self, context):
    available_armatures = []

    for scene_object in bpy.data.objects:
        if scene_object.type == 'ARMATURE':
            available_armatures.append((scene_object.name, scene_object.name, ''))

    return available_armatures

class RetargetAnimationProperties(bpy.types.PropertyGroup):
    # Retarget Animation options
    show_retarget_animation_options: PropertyTypes.Bool(
        description = 'Toggle Retarget Animation Options'
    ) # type: ignore
    retarget_source_armature: PropertyTypes.Enum(
        description = 'Source armature which constraints will be copied from',
        items = get_available_armatures,
    ) # type: ignore
    retarget_target_armature: PropertyTypes.Enum(
        description = 'Target armature which constraints will be copied to',
        items = get_available_armatures,
    ) # type: ignore
