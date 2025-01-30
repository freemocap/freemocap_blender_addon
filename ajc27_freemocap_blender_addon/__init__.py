__author__ = """Skelly FreeMoCap"""
__email__ = "info@freemocap.org"
__version__ = "v2025.01.1035"

#######################################################################
### Add-on to adapt the Freemocap Blender output. It can adjust the
### empties position, add a rig and a body mesh. The resulting rig
### and animation can be imported in platforms like Unreal Engine.
### The rig has a TPose as rest pose for easier retargeting.
### For best results, when the script is ran the empties should be
### forming a standing still pose with arms open similar to A or T Pose
#######################################################################
import logging
import sys
from pathlib import Path

from ajc27_freemocap_blender_addon.utilities.install_dependencies import check_and_install_dependencies

PACKAGE_ROOT_PATH = str(Path(__file__).parent)

root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger = logging.getLogger(__name__)

bl_info = {
    'name': 'freemocap_blender_addon',
    'author': 'ajc27',
    'version': (1, 1, 7),
    'blender': (3, 0, 0),
    'location': '3D Viewport > Sidebar > Freemocap Adapter',
    'description': 'A Blender add-on for loading and visualizing motion capture data recorded with the FreeMoCap software (https://freemocap.org)',
    'category': 'Animation',
}


def unregister():
    import bpy

    try:
        print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Unregistering {__file__} as add-on")
        from .blender_ui import BLENDER_USER_INTERFACE_CLASSES
        for cls in BLENDER_USER_INTERFACE_CLASSES:
            print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Unregistering class {cls.__name__}")
            bpy.utils.unregister_class(cls)

        print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Unregistering property group FREEMOCAP_PROPERTIES")
        del bpy.types.Scene.freemocap_properties
    except Exception as e:
        print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Error unregistering {__file__} as add-on: {e}")


def register():
    import bpy
    print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Checking and/or installing optional dependencies...")
    check_and_install_dependencies()
    print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Registering {__file__} as add-on")
    from .blender_ui import BLENDER_USER_INTERFACE_CLASSES
    print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Registering classes {BLENDER_USER_INTERFACE_CLASSES}")
    for cls in BLENDER_USER_INTERFACE_CLASSES:
        print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Registering class {cls.__name__}")
        bpy.utils.register_class(cls)

        # this is a clunky way to add keymaps (shortcuts) to some operators, we can improve this later
        if cls.__name__ == "FREEMOCAP_load_data":
            # Add the keymap configuration
            wm = bpy.context.window_manager
            km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
            kmi = km.keymap_items.new(cls.bl_idname, 'R', 'PRESS', shift=True, alt=True)
            addon_keymaps.append((km, kmi))
        if cls.__name__ == "FREEMOCAP_clear_scene":
            wm = bpy.context.window_manager
            km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
            kmi = km.keymap_items.new(cls.bl_idname, 'X', 'PRESS', shift=True, alt=True)
            addon_keymaps.append((km, kmi))

    print("[FREEMOCAP-BLENDER-ADDON-INIT] - Registering property group FREEMOCAP_PROPERTIES")

    from ajc27_freemocap_blender_addon.blender_ui import FREEMOCAP_CORE_PROPERTIES, FREEMOCAP_UI_PROPERTIES
    bpy.types.Scene.freemocap_properties = bpy.props.PointerProperty(type=FREEMOCAP_CORE_PROPERTIES)
    bpy.types.Scene.freemocap_ui_properties = bpy.props.PointerProperty(type=FREEMOCAP_UI_PROPERTIES)


    print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Finished registering {__file__} as add-on!")

addon_keymaps = []

if __name__ == "__main__":
    print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Running {__file__} as main file ")
    register()
    print(f"[FREEMOCAP-BLENDER-ADDON-INIT] - Finished running {__file__} as main file!")
