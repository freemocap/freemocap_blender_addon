from pathlib import Path
from typing import Dict

import bpy

from freemocap_blender_addon import PACKAGE_ROOT_PATH
from freemocap_blender_addon.utilities.blender_utilities.print_all_blender_objects import \
    print_all_blender_objects_in_scene

SKELLY_MESH_PREFIX = 'skelly_'

SKELLY_BONE_MESHES_PATH = Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones" / "body" / "axial"

def load_skelly_fbx_files() -> Dict[str, bpy.types.Object]:
    meshes = {}
    for fbx_file_path in SKELLY_BONE_MESHES_PATH.glob("*.fbx"):
        bpy.ops.import_scene.fbx(filepath=str(fbx_file_path))
        mesh_name = fbx_file_path.stem
        meshes[mesh_name] = bpy.data.objects[mesh_name]

if __name__ == "__main__":
    import pprint
    pprint.pprint("Loading skelly meshes....")
    load_skelly_fbx_files()
    print_all_blender_objects_in_scene()
    pprint.pprint(bpy.data.objects.keys())
