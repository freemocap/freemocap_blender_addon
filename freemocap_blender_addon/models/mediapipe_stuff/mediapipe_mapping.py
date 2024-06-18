from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BodyKeypoints
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.keypoint_mapping_abc import \
    KeypointMappingsEnum


class MediapipeBodyMapping(KeypointMappingsEnum):
    NOSE_TIP = ["nose"]
    RIGHT_EYE_INNER = ["right_eye_inner"]
    RIGHT_EYE_CENTER = ["right_eye"]
    RIGHT_EYE_OUTER = ["right_eye_outer"]
    RIGHT_EAR_TRAGUS = ["right_ear"]
    RIGHT_MOUTH = ["mouth_right"]
    LEFT_EYE_INNER = ["left_eye_inner"]
    LEFT_EYE_CENTER = ["left_eye"]
    LEFT_EYE_OUTER = ["left_eye_outer"]
    LEFT_EAR_TRAGUS = ["left_ear"]
    LEFT_MOUTH = ["mouth_left"]
    SKULL_CENTER_FORAMEN_MAGNUM = {"left_ear": .45, "right_ear": .45, "left_shoulder": .05, "right_shoulder": .05}
    NECK_TOP_ATLAS_C1 = {"left_ear": .4, "right_ear": .4, "left_shoulder": .1, "right_shoulder": .1}
    NECK_BASE_C7 = ["left_shoulder", "right_shoulder"]
    CHEST_CENTER_T12 = ["left_hip", "right_hip", "left_shoulder", "right_shoulder"]
    PELVIS_CENTER = ["left_hip", "right_hip"]
    # RIGHT_CLAVICLE = {"right_shoulder": .55, "left_shoulder": .45},
    RIGHT_SHOULDER = ["right_shoulder"]
    RIGHT_ELBOW = ["right_elbow"]
    RIGHT_WRIST = ["right_wrist"]
    RIGHT_INDEX_KNUCKLE = ["right_index"]
    RIGHT_PINKY_KNUCKLE = ["right_pinky"]
    RIGHT_THUMB_KNUCKLE = ["right_thumb"]
    RIGHT_HIP = ["right_hip"]
    RIGHT_KNEE = ["right_knee"]
    RIGHT_ANKLE = ["right_ankle"]
    RIGHT_HEEL = ["right_heel"]
    RIGHT_HALLUX_TIP = ["right_foot_index"]
    # LEFT_CLAVICLE = {"left_shoulder": .55, "right_shoulder": .45},
    LEFT_SHOULDER = ["left_shoulder"]
    LEFT_ELBOW = ["left_elbow"]
    LEFT_WRIST = ["left_wrist"]
    LEFT_INDEX_KNUCKLE = ["left_index"]
    LEFT_PINKY_KNUCKLE = ["left_pinky"]
    LEFT_THUMB_KNUCKLE = ["left_thumb"]
    LEFT_HIP = ["left_hip"]
    LEFT_KNEE = ["left_knee"]
    LEFT_ANKLE = ["left_ankle"]
    LEFT_HEEL = ["left_heel"]
    LEFT_HALLUX_TIP = ["left_foot_index"]


for key in MediapipeBodyMapping.__members__.keys():
    missing_keys = []
    if not hasattr(BodyKeypoints, key):
        missing_keys.append(key)
    if missing_keys:
        raise ValueError(f"Keys [{missing_keys}] are missing from BodyKeypoints")

print(f"MediapipeBodyMapping enum created successfully with {len(MediapipeBodyMapping.__members__)} keys\n")
print("\n".join([f"{key}: {value.value}" for key, value in MediapipeBodyMapping.__members__.items()]))
