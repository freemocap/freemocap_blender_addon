import bpy

from ajc27_freemocap_blender_addon.core_functions.com_bos.add_com_vertical_projection import add_com_vertical_projection

class FREEMOCAP_OT_add_com_vertical_projection(bpy.types.Operator):
    bl_idname = 'freemocap._add_com_vertical_projection'
    bl_label = 'Add COM Vertical Projection'
    bl_description = "Add COM Vertical Projection"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Adding COM Vertical Projection.......")
        data_parent_empty = context.scene.freemocap_properties.data_parent_empty
        # Add COM Vertical Projection
        add_com_vertical_projection(data_parent_empty=data_parent_empty,
                                    neutral_color=context.scene.freemocap_ui_properties.com_vertical_projection_neutral_color,
                                    in_bos_color=context.scene.freemocap_ui_properties.com_vertical_projection_in_bos_color,
                                    out_bos_color=context.scene.freemocap_ui_properties.com_vertical_projection_out_bos_color)

        # Set the show COM Vertical Projection property to True
        context.scene.freemocap_ui_properties.show_com_vertical_projection = True

        return {'FINISHED'}


