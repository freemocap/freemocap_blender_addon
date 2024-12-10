from typing import Dict

from freemocap_blender_addon.data_models.bones.bone_definition_models import BoneStatistics


def calculate_body_dimensions(bone_stats: Dict[str, BoneStatistics]) -> Dict[str, float]:
    left_shin_length = bone_stats["shin.L"].median
    left_thigh_length = bone_stats["thigh.L"].median
    left_leg_length_minus_ankle_height = left_shin_length + left_thigh_length
    left_leg_length = left_leg_length_minus_ankle_height * 1.079  # correct for ankle height - according to Winter 1995 anthropmetry, ankle height is ~7.9% of leg length

    right_shin_length = bone_stats["shin.R"].median
    right_thigh_length = bone_stats["thigh.R"].median
    right_leg_length_minus_ankle_height = right_shin_length + right_thigh_length
    right_leg_length = right_leg_length_minus_ankle_height * 1.079

    mean_leg_length = (left_leg_length + right_leg_length) / 2

    torso_length = bone_stats["spine"].median + bone_stats["spine.001"].median + bone_stats["neck"].median

    total_height_minus_half_head = mean_leg_length + torso_length
    total_height = total_height_minus_half_head * 1.064  # correct for half head height - according to Winter 1995 anthropmetry, ground to head_center is ~93.6% of total height

    left_hand_length = bone_stats["f_middle.03.L"].median + bone_stats["f_middle.02.L"].median + \
                       bone_stats["f_middle.01.L"].median + bone_stats["palm.02.L"].median
    left_forearm_length = bone_stats["forearm.L"].median
    left_upperarm_length = bone_stats["upper_arm.L"].median
    left_shoulder_length = bone_stats["shoulder.L"].median
    left_arm_length = left_hand_length + left_forearm_length + left_upperarm_length + left_shoulder_length

    right_hand_length = bone_stats["f_middle.03.R"].median + bone_stats["f_middle.02.R"].median + \
                        bone_stats["f_middle.01.R"].median + bone_stats["palm.02.R"].median
    right_forearm_length = bone_stats["forearm.R"].median
    right_upperarm_length = bone_stats["upper_arm.R"].median
    right_shoulder_length = bone_stats["shoulder.R"].median
    right_arm_length = right_hand_length + right_forearm_length + right_upperarm_length + right_shoulder_length

    total_wingspan = left_arm_length + right_arm_length

    left_fore_foot_length = bone_stats["foot.L"].median
    left_heel_length = bone_stats["heel.02.L"].median
    left_foot_length = left_fore_foot_length + left_heel_length * .7  # correction for the fact that these bones are at an angle - this one is just eyeballed lol

    right_fore_foot_length = bone_stats["foot.R"].median
    right_heel_length = bone_stats["heel.02.R"].median
    right_foot_length = right_fore_foot_length + right_heel_length * .7  # correction for the fact that these bones are at an angle - this one is just eyeballed lol

    mean_foot_length = (left_foot_length + right_foot_length) / 2

    return {
        "total_height": total_height,
        "total_wingspan": total_wingspan,
        "mean_foot_length": mean_foot_length,
    }
