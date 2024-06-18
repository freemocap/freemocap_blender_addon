from pathlib import Path
import bpy

base_path = Path(r"/freemocap_blender_addon/assets/skelly_bones")
body_bones_path = base_path / "body"
axial_bones_path = body_bones_path / "axial"

mesh_filename = 'skelly_lumbar_spine.fbx'
bpy.ops.import_scene.fbx(filepath=str(axial_bones_path/mesh_filename))