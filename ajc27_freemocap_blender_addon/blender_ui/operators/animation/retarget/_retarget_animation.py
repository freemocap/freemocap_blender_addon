import bpy


class FREEMOCAP_OT_retarget_animation(bpy.types.Operator):
    bl_idname = 'freemocap._retarget_animation'
    bl_label = 'Retarget Animation'
    bl_description = "Retarget Animation"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        animation_props = context.scene.freemocap_ui_properties.retarget_animation_properties

        print("Retargeting animation.......")
        for pair in animation_props.retarget_pairs:
            print(f"Source Bone: {pair.source_bone}, Target Bone: {pair.target_bone}")

        source_armature = animation_props.retarget_source_armature
        target_armature = animation_props.retarget_target_armature

        if source_armature != target_armature:
            # Add a copy rotation constraint to each target bone
            for pair in animation_props.retarget_pairs:
                bone_constraint = bpy.data.objects[target_armature].pose.bones[pair.target_bone].constraints.new(
                        'COPY_ROTATION'
                )
                bone_constraint.target = bpy.data.objects[source_armature]
                bone_constraint.subtarget = bpy.data.objects[source_armature].pose.bones[pair.source_bone].name
            
            # Add a copy location constraint to the root bone of the target armature
            bone_constraint = bpy.data.objects[target_armature].pose.bones[animation_props.retarget_target_root_bone].constraints.new(
                'COPY_LOCATION'
            )
            bone_constraint.target = bpy.data.objects[source_armature]
            bone_constraint.subtarget = bpy.data.objects[source_armature].pose.bones[animation_props.retarget_source_root_bone].name
            bone_constraint.use_offset = True
            bone_constraint.target_space = 'LOCAL'

        return {'FINISHED'}
    