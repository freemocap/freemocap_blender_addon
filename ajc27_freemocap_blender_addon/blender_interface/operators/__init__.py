from ajc27_freemocap_blender_addon.blender_interface.operators._clear_scene import FMC_ADAPTER_clear_scene
from ajc27_freemocap_blender_addon.blender_interface.operators._run_all import FMC_ADAPTER_run_all

#
# from ajc27_freemocap_blender_addon.blender_interface.operators._add_body_mesh import FMC_ADAPTER_OT_add_body_mesh
# from ajc27_freemocap_blender_addon.blender_interface.operators._add_rig import FMC_ADAPTER_OT_add_rig
# from ajc27_freemocap_blender_addon.blender_interface.operators._export_fbx import FMC_ADAPTER_OT_export_fbx
# from ajc27_freemocap_blender_addon.blender_interface.operators._load_freemocap_data import FMC_ADAPTER_load_freemocap_data
# from ajc27_freemocap_blender_addon.blender_interface.operators._load_videos import FMC_ADAPTER_load_videos
# from ajc27_freemocap_blender_addon.blender_interface.operators._reduce_bone_length_dispersion import \
#     FMC_ADAPTER_OT_reduce_bone_length_dispersion
# from ajc27_freemocap_blender_addon.blender_interface.operators._reduce_shakiness import FMC_ADAPTER_OT_reduce_shakiness
# from ajc27_freemocap_blender_addon.blender_interface.operators._reorient_empties import FMC_ADAPTER_OT_reorient_empties
# from ajc27_freemocap_blender_addon.blender_interface.operators._save_out_data import FMC_ADAPTER_save_data_to_disk

BLENDER_OPERATORS = [  # FMC_ADAPTER_download_sample_data,
    FMC_ADAPTER_clear_scene,
    FMC_ADAPTER_run_all,
    # FMC_ADAPTER_save_data_to_disk,
    # FMC_ADAPTER_load_videos,
    # FMC_ADAPTER_load_freemocap_data,
    # FMC_ADAPTER_OT_reorient_empties,
    # FMC_ADAPTER_OT_reduce_bone_length_dispersion,
    # FMC_ADAPTER_OT_reduce_shakiness,
    # FMC_ADAPTER_OT_add_rig,
    # FMC_ADAPTER_OT_add_body_mesh,
    # FMC_ADAPTER_OT_export_fbx,
]
