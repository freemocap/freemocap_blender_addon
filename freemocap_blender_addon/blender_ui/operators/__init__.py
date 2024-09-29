from freemocap_blender_addon.blender_ui.operators._add_base_of_support import FREEMOCAP_OT_add_base_of_support
from freemocap_blender_addon.blender_ui.operators._add_com_vertical_projection import \
    FREEMOCAP_OT_add_com_vertical_projection
from freemocap_blender_addon.blender_ui.operators._add_joint_angles import FREEMOCAP_OT_add_joint_angles
from freemocap_blender_addon.blender_ui.operators._clear_scene import FREEMOCAP_OT_clear_scene
from freemocap_blender_addon.blender_ui.operators._create_video import FREEMOCAP_OT_create_video
from freemocap_blender_addon.blender_ui.operators._load_data import FREEMOCAP_OT_load_data




BLENDER_OPERATORS = [  # FREEMOCAP_download_sample_data,
    FREEMOCAP_OT_clear_scene,
    FREEMOCAP_OT_load_data,
    FREEMOCAP_OT_add_com_vertical_projection,
    FREEMOCAP_OT_add_joint_angles,
    FREEMOCAP_OT_add_base_of_support,
    FREEMOCAP_OT_create_video,

]
