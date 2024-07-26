from typing import Any, Dict

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import BoneDefinition


def calculate_body_dimensions(bones_info: Dict[str, BoneDefinition]) -> Dict[str, float]:
    left_shin_length = bones_info["shin.L"].median
    left_thigh_length = bones_info["thigh.L"].median
    left_leg_length_minus_ankle_height = left_shin_length + left_thigh_length
    left_leg_length = left_leg_length_minus_ankle_height * 1.079  # correct for ankle height - according to Winter 1995 anthropmetry, ankle height is ~7.9% of leg length

    right_shin_length = bones_info["shin.R"].median
    right_thigh_length = bones_info["thigh.R"].median
    right_leg_length_minus_ankle_height = right_shin_length + right_thigh_length
    right_leg_length = right_leg_length_minus_ankle_height * 1.079

    mean_leg_length = (left_leg_length + right_leg_length) / 2

    torso_length = bones_info["spine"].median + bones_info["spine.001"].median + bones_info["neck"].median

    total_height_minus_half_head = mean_leg_length + torso_length
    total_height = total_height_minus_half_head * 1.064  # correct for half head height - according to Winter 1995 anthropmetry, ground to head_center is ~93.6% of total height

    left_hand_length = bones_info["f_middle.03.L"].median + bones_info["f_middle.02.L"].median + \
                       bones_info["f_middle.01.L"].median + bones_info["palm.02.L"].median
    left_forearm_length = bones_info["forearm.L"].median
    left_upperarm_length = bones_info["upper_arm.L"].median
    left_shoulder_length = bones_info["shoulder.L"].median
    left_arm_length = left_hand_length + left_forearm_length + left_upperarm_length + left_shoulder_length

    right_hand_length = bones_info["f_middle.03.R"].median + bones_info["f_middle.02.R"].median + \
                        bones_info["f_middle.01.R"].median + bones_info["palm.02.R"].median
    right_forearm_length = bones_info["forearm.R"].median
    right_upperarm_length = bones_info["upper_arm.R"].median
    right_shoulder_length = bones_info["shoulder.R"].median
    right_arm_length = right_hand_length + right_forearm_length + right_upperarm_length + right_shoulder_length

    total_wingspan = left_arm_length + right_arm_length

    left_fore_foot_length = bones_info["foot.L"].median
    left_heel_length = bones_info["heel.02.L"].median
    left_foot_length = left_fore_foot_length + left_heel_length * .7  # correction for the fact that these bones are at an angle - this one is just eyeballed lol

    right_fore_foot_length = bones_info["foot.R"].median
    right_heel_length = bones_info["heel.02.R"].median
    right_foot_length = right_fore_foot_length + right_heel_length * .7  # correction for the fact that these bones are at an angle - this one is just eyeballed lol

    mean_foot_length = (left_foot_length + right_foot_length) / 2

    return {
        "total_height": total_height,
        "total_wingspan": total_wingspan,
        "mean_foot_length": mean_foot_length,
    }
