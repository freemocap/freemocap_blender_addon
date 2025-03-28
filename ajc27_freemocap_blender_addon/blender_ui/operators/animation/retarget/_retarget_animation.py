import bpy


class FREEMOCAP_OT_retarget_animation(bpy.types.Operator):
    bl_idname = 'freemocap._retarget_animation'
    bl_label = 'Retarget Animation'
    bl_description = "Retarget Animation"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        animation_props = context.scene.freemocap_ui_properties.retarget_animation_properties

        print("Retargeting animation.......")

        source_armature_name = animation_props.retarget_source_armature
        target_armature_name = animation_props.retarget_target_armature

        if source_armature_name != target_armature_name:
            source_armature = bpy.data.objects[source_armature_name]
            target_armature = bpy.data.objects[target_armature_name]
            # Add a copy rotation constraint to each target bone
            for pair in animation_props.retarget_pairs:
                if pair.target_bone:
                    bone_constraint = target_armature.pose.bones[pair.target_bone].constraints.new(
                            'COPY_ROTATION'
                    )
                    bone_constraint.target = source_armature
                    bone_constraint.subtarget = source_armature.pose.bones[pair.source_bone].name
                
            # Add a copy location constraint to the root bone of the target armature
            if animation_props.retarget_target_root_bone == 'Object_origin':
                bone_constraint = target_armature.constraints.new('COPY_LOCATION')
                bone_constraint.target = source_armature
                bone_constraint.subtarget = source_armature.pose.bones[animation_props.retarget_source_root_bone].name
                bone_constraint.use_offset = True
                bone_constraint.target_space = 'LOCAL'
            else:
                bone_constraint = target_armature.pose.bones[animation_props.retarget_target_root_bone].constraints.new(
                    'COPY_LOCATION'
                )
                bone_constraint.target = source_armature
                bone_constraint.subtarget = source_armature.pose.bones[animation_props.retarget_source_root_bone].name
                bone_constraint.use_offset = True
                bone_constraint.target_space = 'LOCAL'

        return {'FINISHED'}
    