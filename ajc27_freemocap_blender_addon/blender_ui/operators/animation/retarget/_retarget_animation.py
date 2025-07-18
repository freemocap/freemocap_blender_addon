import bpy
import math

from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.ui_utilities import get_edit_bones_adjusted_axes

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

            # Get the adjusted axes of the edit bones
            source_bones_adjusted_axes = get_edit_bones_adjusted_axes(
                source_armature,
                animation_props.retarget_source_x_axis_convention,
                animation_props.retarget_source_y_axis_convention,
                animation_props.retarget_source_z_axis_convention
            )
            target_bones_adjusted_axes = get_edit_bones_adjusted_axes(
                target_armature,
                animation_props.retarget_target_x_axis_convention,
                animation_props.retarget_target_y_axis_convention,
                animation_props.retarget_target_z_axis_convention
            )

            #  Select the target armature
            target_armature.select_set(True)
            # Set Edit Mode
            bpy.ops.object.mode_set(mode="EDIT")

            # For each one of the retarget pairs, get the angle between 
            # the source and target x axes and add that angle to the
            # roll value of the target bone
            for pair in animation_props.retarget_pairs:
                if pair.target_bone:
                    angle = source_bones_adjusted_axes[pair.source_bone][0].angle(
                        target_bones_adjusted_axes[pair.target_bone][0]
                    )
                    # Calculate the cross product of the two vectors
                    cross_product = target_bones_adjusted_axes[pair.target_bone][0].cross(
                        source_bones_adjusted_axes[pair.source_bone][0]
                    )
                    # Get the dot product of the cross product and the
                    # y axis of the target bone
                    dot_product = cross_product.dot(
                        target_bones_adjusted_axes[pair.target_bone][1]
                    )
                    # If the dot product is negative, multiply the angle by -1
                    if dot_product < 0:
                        angle *= -1

                    #  Set the adjusted bone roll
                    current_roll = target_armature.data.edit_bones[pair.target_bone].roll
                    target_armature.data.edit_bones[pair.target_bone].roll = current_roll + angle

            # Add a copy rotation constraint to each target bone
            for pair in animation_props.retarget_pairs:
                if pair.target_bone:
                    bone_constraint = target_armature.pose.bones[pair.target_bone].constraints.new(
                            'COPY_ROTATION'
                    )
                    bone_constraint.target = source_armature
                    bone_constraint.subtarget = source_armature.pose.bones[pair.source_bone].name
                    bone_constraint.mix_mode = animation_props.retarget_target_bone_rotation_mixmode
                    bone_constraint.target_space = animation_props.retarget_target_bone_rotation_target_space
                    bone_constraint.owner_space = animation_props.retarget_target_bone_rotation_owner_space

                    if pair.target_bone == animation_props.retarget_target_root_bone:
                        bone_constraint.mix_mode = 'OFFSET'
                        bone_constraint.target_space = 'WORLD'
                        bone_constraint.owner_space = 'WORLD'

            # Set Object Mode
            bpy.ops.object.mode_set(mode="OBJECT")
                
            # Add a copy location constraint to the root bone of the target armature
            # Add it to the armture itself if there is no root bone
            if animation_props.retarget_target_root_bone == 'Armature_origin':
                bone_location_constraint = target_armature.constraints.new('COPY_LOCATION')

                armature_rotation_constraint = target_armature.constraints.new('COPY_ROTATION')
                armature_rotation_constraint.target = source_armature
                armature_rotation_constraint.subtarget = source_armature.pose.bones[animation_props.retarget_source_root_bone].name
                armature_rotation_constraint.mix_mode = 'OFFSET'
                armature_rotation_constraint.target_space = 'LOCAL'

            else:
                bone_location_constraint = target_armature.pose.bones[animation_props.retarget_target_root_bone].constraints.new(
                    'COPY_LOCATION'
                )

            bone_location_constraint.target = source_armature
            bone_location_constraint.subtarget = source_armature.pose.bones[animation_props.retarget_source_root_bone].name
            bone_location_constraint.use_offset = True
            bone_location_constraint.target_space = 'LOCAL'

        return {'FINISHED'}
    