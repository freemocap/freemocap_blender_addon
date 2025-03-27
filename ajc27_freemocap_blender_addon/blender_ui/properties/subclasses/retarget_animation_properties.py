import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

def get_available_armatures(self, context):
    available_armatures = []

    for scene_object in bpy.data.objects:
        if scene_object.type == 'ARMATURE':
            available_armatures.append((scene_object.name, scene_object.name, ''))

    return available_armatures

class RetargetBonePair(bpy.types.PropertyGroup):
    source_bone: PropertyTypes.String(
        name="Source Bone"
    ) # type: ignore
    target_bone: PropertyTypes.String(
        name="Target Bone"
    ) # type: ignore

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
    retarget_pairs: PropertyTypes.Collection(
        type=RetargetBonePair
    ) # type: ignore
    active_pair_index: PropertyTypes.Int() # type: ignore

# Custom UI list
class UL_RetargetPairs(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        
        # Source bone name
        row.label(text=item.source_bone)
        
        # Target bone selector
        target_armature = context.scene.freemocap_ui_properties.retarget_animation_properties.retarget_target_armature
        if target_armature and bpy.data.objects[target_armature].type == 'ARMATURE':
            row.prop_search(
                item,
                "target_bone",
                bpy.data.objects[target_armature].data,
                "bones",
                text="",
                icon='BONE_DATA'
            )
        else:
            row.label(text="No target armature")
