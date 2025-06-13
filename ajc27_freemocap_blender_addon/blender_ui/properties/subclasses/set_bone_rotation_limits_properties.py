import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

class SetBoneRotationLimitsProperties(bpy.types.PropertyGroup):
    show_set_bone_rotation_limits_options: PropertyTypes.Bool(
        description = 'Toggle Set Bone Rotation Limits Options'
    ) # type: ignore
