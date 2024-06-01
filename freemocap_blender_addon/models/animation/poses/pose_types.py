from freemocap_blender_addon.models.animation.poses.freemocap_apose import freemocap_apose
from freemocap_blender_addon.models.animation.poses.freemocap_tpose import freemocap_tpose
from freemocap_blender_addon.models.animation.poses.ue_metahuman_default import ue_metahuman_default
from freemocap_blender_addon.models.animation.poses.ue_metahuman_tpose import ue_metahuman_tpose


class PoseType:
    FREEMOCAP_APOSE = freemocap_apose
    FREEMOCAP_TPOSE = freemocap_tpose
    UE_METAHUMAN_DEFAULT = ue_metahuman_default
    UE_METAHUMAN_TPOSE = ue_metahuman_tpose
