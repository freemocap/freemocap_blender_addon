import bpy
import bpy_extras


class FMC_ADAPTER_download_sample_data(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = 'fmc_adapter._download_sample_data'
    bl_label = "Download Sample Data"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Downloading sample data....")
        download_sample_data()
        return {'FINISHED'}
