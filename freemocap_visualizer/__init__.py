bl_info = {
    'name'          : 'Freemocap Visualizer',
    'author'        : 'ajc27',
    'version'       : (1, 1, 0),
    'blender'       : (3, 0, 0),
    'location'      : '3D Viewport > Sidebar > Freemocap Visualizer',
    'description'   : 'Add-on to help visualize the Freemocap Blender output',
    'category'      : 'Development',
}

import bpy
from .addon_interface import (FMC_VISUALIZER_PROPERTIES,
                              VIEW3D_PT_freemocap_visualizer,
                              FMC_VISUALIZER_ADD_COM_VERTICAL_PROJECTION,
                              FMC_VISUALIZER_ADD_JOINT_ANGLES,
                              FMC_VISUALIZER_ADD_BASE_OF_SUPPORT)

def register():

    # Register addon classes
    bpy.utils.register_class(FMC_VISUALIZER_PROPERTIES)
    bpy.utils.register_class(VIEW3D_PT_freemocap_visualizer)
    bpy.utils.register_class(FMC_VISUALIZER_ADD_COM_VERTICAL_PROJECTION)
    bpy.utils.register_class(FMC_VISUALIZER_ADD_JOINT_ANGLES)
    bpy.utils.register_class(FMC_VISUALIZER_ADD_BASE_OF_SUPPORT)

    bpy.types.Scene.fmc_visualizer_tool = bpy.props.PointerProperty(type = FMC_VISUALIZER_PROPERTIES)

def unregister():
    
    # Unregister addon classes
    bpy.utils.unregister_class(FMC_VISUALIZER_PROPERTIES)
    bpy.utils.unregister_class(VIEW3D_PT_freemocap_visualizer)
    bpy.utils.unregister_class(FMC_VISUALIZER_ADD_COM_VERTICAL_PROJECTION)
    bpy.utils.unregister_class(FMC_VISUALIZER_ADD_JOINT_ANGLES)
    bpy.utils.unregister_class(FMC_VISUALIZER_ADD_BASE_OF_SUPPORT)
    
    del bpy.types.Scene.fmc_visualizer_tool

if __name__ == "__main__":
    register()
