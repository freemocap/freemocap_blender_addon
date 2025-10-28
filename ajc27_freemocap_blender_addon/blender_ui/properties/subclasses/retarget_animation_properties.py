import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

def get_available_armatures(self, context):
    available_armatures = []

    for scene_object in bpy.data.objects:
        if scene_object.type == 'ARMATURE':
            available_armatures.append((scene_object.name, scene_object.name, ''))

    return available_armatures

def get_available_bones(self, context, retarget_side):
    if retarget_side == 'source':
        armature = bpy.data.objects[self.retarget_source_armature]
    elif retarget_side == 'target':
        armature = bpy.data.objects[self.retarget_target_armature]

    available_bones = []

    # Append the bones to the list but put at the beginning the ones
    # that are part of the list ['root', 'pelvis']
    for bone in armature.pose.bones:
        if bone.name in ['root', 'pelvis']:
            available_bones.insert(0, (bone.name, bone.name, ''))
        else:
            available_bones.append((bone.name, bone.name, ''))

    # Add a Object_origin bone for those armatures without root or pelvis bones
    if 'root' not in armature.pose.bones and 'pelvis' not in armature.pose.bones:
        available_bones.insert(0, ('Armature_origin', 'Armature_origin', ''))
    else:
        available_bones.insert(1, ('Armature_origin', 'Armature_origin', ''))

    return available_bones


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
    retarget_source_root_bone: PropertyTypes.Enum(
        description = 'Root bone of the source armature. In case there are no bones like root or pelvis, the armature origin can be used',
        items = lambda a,b: get_available_bones(
            a,
            b,
            'source')
    ) # type: ignore
    retarget_target_root_bone: PropertyTypes.Enum(
        description = 'Root bone of the target armature. In case there are no bones like root or pelvis, the armature origin can be used',
        items = lambda a,b: get_available_bones(
            a,
            b,
            'target')
    ) # type: ignore
    retarget_source_x_axis_convention: PropertyTypes.Enum(
        description = 'The source armature local x axis convention. '
            + 'Before retargeting, the local axes of the source armature will be converted to xyz. '
            + 'Some common conventions are: Mixamo=x-zy.',
        items = [
            ('x', 'x', ''),
            ('y', 'y', ''),
            ('z', 'z', ''),
            ('-x', '-x', ''),
            ('-y', '-y', ''),
            ('-z', '-z', ''),
        ]
    ) # type: ignore
    retarget_source_y_axis_convention: PropertyTypes.Enum(
        description = 'The source armature local y axis convention. '
            + 'Before retargeting, the local axes of the source armature will be converted to xyz. '
            + 'Some common conventions are: Mixamo=x-zy.',
        items = [
            ('y', 'y', ''),
            ('x', 'x', ''),
            ('z', 'z', ''),
            ('-x', '-x', ''),
            ('-y', '-y', ''),
            ('-z', '-z', ''),
        ]
    ) # type: ignore
    retarget_source_z_axis_convention: PropertyTypes.Enum(
        description = 'The source armature local z axis convention. '
            + 'Before retargeting, the local axes of the source armature will be converted to xyz. '
            + 'Some common conventions are: Mixamo=x-zy.',
        items = [
            ('z', 'z', ''),
            ('x', 'x', ''),
            ('y', 'y', ''),
            ('-x', '-x', ''),
            ('-y', '-y', ''),
            ('-z', '-z', ''),
        ]
    ) # type: ignore
    retarget_target_x_axis_convention: PropertyTypes.Enum(
        description = 'The target armature local x axis convention. '
            + 'Before retargeting, the local axes of the source armature will be converted to xyz. '
            + 'Some common conventions are: Mixamo=x-zy.',
        items = [
            ('x', 'x', ''),
            ('y', 'y', ''),
            ('z', 'z', ''),
            ('-x', '-x', ''),
            ('-y', '-y', ''),
            ('-z', '-z', ''),
        ]
    ) # type: ignore
    retarget_target_y_axis_convention: PropertyTypes.Enum(
        description = 'The target armature local y axis convention. '
            + 'Before retargeting, the local axes of the source armature will be converted to xyz. '
            + 'Some common conventions are: Mixamo=x-zy.',
        items = [
            ('y', 'y', ''),
            ('x', 'x', ''),
            ('z', 'z', ''),
            ('-x', '-x', ''),
            ('-y', '-y', ''),
            ('-z', '-z', ''),
        ]
    ) # type: ignore
    retarget_target_z_axis_convention: PropertyTypes.Enum(
        description = 'The target armature local z axis convention. '
            + 'Before retargeting, the local axes of the source armature will be converted to xyz. '
            + 'Some common conventions are: Mixamo=x-zy.',
        items = [
            ('z', 'z', ''),
            ('x', 'x', ''),
            ('y', 'y', ''),
            ('-x', '-x', ''),
            ('-y', '-y', ''),
            ('-z', '-z', ''),
        ]
    ) # type: ignore
    retarget_target_bone_rotation_mixmode: PropertyTypes.Enum(
        description = 'Mix Mode to use in the Copy Rotation bone constraint',
        items = [
            ('OFFSET', 'Offset (Legacy)', ''),
            ('REPLACE', 'Replace', ''),
            ('ADD', 'Add', ''),
            ('BEFORE', 'Before Original', ''),
            ('AFTER', 'After Original', ''),
        ]
    ) # type: ignore
    retarget_target_bone_rotation_target_space: PropertyTypes.Enum(
        description = 'Target Space to use in the Copy Rotation bone constraint',
        items = [
            ('LOCAL', 'Local Space', ''),
            ('WORLD', 'World Space', ''),
            ('CUSTOM', 'Custom Space', ''),
            ('POSE', 'Pose Space', ''),
            ('LOCAL_WITH_PARENT', 'Local With Parent', ''),
            ('LOCAL_OWNER_ORIENT', 'Local Space (Owner Orientation)', '')
        ]
    ) # type: ignore
    retarget_target_bone_rotation_owner_space: PropertyTypes.Enum(
        description = 'Owner Space to use in the Copy Rotation bone constraint',
        items = [
            ('LOCAL', 'Local Space', ''),
            ('WORLD', 'World Space', ''),
            ('CUSTOM', 'Custom Space', ''),
            ('POSE', 'Pose Space', ''),
            ('LOCAL_WITH_PARENT', 'Local With Parent', '')
        ]
    ) # type: ignore
    retarget_pairs: PropertyTypes.Collection(
        type=RetargetBonePair
    ) # type: ignore
    active_pair_index: PropertyTypes.Int() # type: ignore

# Custom UI list
class ANIMATION_UL_RetargetPairs(bpy.types.UIList):
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
