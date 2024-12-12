from ajc27_freemocap_blender_addon.data_models.armatures.freemocap_armature_definition import armature_freemocap
from ajc27_freemocap_blender_addon.data_models.armatures.ue_metahuman_simple import armature_ue_metahuman_simple
from ajc27_freemocap_blender_addon.data_models.poses.freemocap_apose import freemocap_apose
from ajc27_freemocap_blender_addon.data_models.poses.freemocap_tpose import freemocap_tpose
from ajc27_freemocap_blender_addon.data_models.poses.ue_metahuman_default import ue_metahuman_default
from ajc27_freemocap_blender_addon.data_models.poses.ue_metahuman_tpose import ue_metahuman_tpose

class ArmatureType:
    FREEMOCAP = armature_freemocap
    UE_METAHUMAN_SIMPLE = armature_ue_metahuman_simple

class PoseType:
    FREEMOCAP_APOSE = freemocap_apose
    FREEMOCAP_TPOSE = freemocap_tpose
    UE_METAHUMAN_DEFAULT = ue_metahuman_default
    UE_METAHUMAN_TPOSE = ue_metahuman_tpose