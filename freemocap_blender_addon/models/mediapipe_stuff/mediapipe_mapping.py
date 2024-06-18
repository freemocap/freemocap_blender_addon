from enum import auto

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BodyKeypoints as bk
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.keypoint_mapping_abc import \
    KeypointMappingsEnum
from freemocap_blender_addon.utilities.blender_utilities.blenderize_name import BlenderizableEnum


class MediapipeTrackedPointNames(BlenderizableEnum):
    NOSE = auto()
    LEFT_EYE_INNER = auto()
    LEFT_EYE = auto()
    LEFT_EYE_OUTER = auto()
    RIGHT_EYE_INNER = auto()
    RIGHT_EYE = auto()
    RIGHT_EYE_OUTER = auto()
    LEFT_EAR = auto()
    RIGHT_EAR = auto()
    MOUTH_LEFT = auto()
    MOUTH_RIGHT = auto()
    LEFT_SHOULDER = auto()
    RIGHT_SHOULDER = auto()
    LEFT_ELBOW = auto()
    RIGHT_ELBOW = auto()
    LEFT_WRIST = auto()
    RIGHT_WRIST = auto()
    LEFT_INDEX = auto()
    RIGHT_INDEX = auto()
    LEFT_PINKY = auto()
    RIGHT_PINKY = auto()
    LEFT_THUMB = auto()
    RIGHT_THUMB = auto()
    LEFT_HIP = auto()
    RIGHT_HIP = auto()
    LEFT_KNEE = auto()
    RIGHT_KNEE = auto()
    LEFT_ANKLE = auto()
    RIGHT_ANKLE = auto()
    LEFT_HEEL = auto()
    RIGHT_HEEL = auto()
    RIGHT_FOOT_INDEX = auto()
    LEFT_FOOT_INDEX = auto()

    def lower(self) -> str:
        return self.name.lower()


mtpn = MediapipeTrackedPointNames

_MEDIAPIPE_BODY_MAPPING = {
    bk.SKULL_FORWARD_NOSE_TIP.name: [mtpn.NOSE.lower()],
    bk.RIGHT_SKULL_EYE_INNER.name: [mtpn.RIGHT_EYE_INNER.lower()],
    bk.RIGHT_SKULL_EYE_CENTER.name: [mtpn.RIGHT_EYE.lower()],
    bk.RIGHT_SKULL_EYE_OUTER.name: [mtpn.RIGHT_EYE_OUTER.lower()],
    bk.RIGHT_SKULL_ACOUSTIC_MEATUS.name: [mtpn.RIGHT_EAR.lower()],
    bk.RIGHT_SKULL_CANINE_TOOTH_TIP.name: [mtpn.MOUTH_RIGHT.lower()],
    bk.LEFT_SKULL_EYE_INNER.name: [mtpn.LEFT_EYE_INNER.lower()],
    bk.LEFT_SKULL_EYE_CENTER.name: [mtpn.LEFT_EYE.lower()],
    bk.LEFT_SKULL_EYE_OUTER.name: [mtpn.LEFT_EYE_OUTER.lower()],
    bk.LEFT_SKULL_ACOUSTIC_MEATUS.name: [mtpn.LEFT_EAR.lower()],
    bk.LEFT_SKULL_CANINE_TOOTH_TIP.name: [mtpn.MOUTH_LEFT.lower()],
    bk.SKULL_ORIGIN_FORAMEN_MAGNUM.name: [mtpn.LEFT_EAR.lower(),
                                          mtpn.RIGHT_EAR.lower()],
    bk.CERVICAL_SPINE_TOP_C1_AXIS.name: {mtpn.LEFT_EAR.lower(): .45,
                                         mtpn.RIGHT_EAR.lower(): .45,
                                         mtpn.LEFT_SHOULDER.lower(): .05,
                                         mtpn.RIGHT_SHOULDER.lower(): .05},
    bk.CERVICAL_SPINE_ORIGIN_C7.name: {mtpn.LEFT_EAR.lower(): .4,
                                       mtpn.RIGHT_EAR.lower(): .4,
                                       mtpn.LEFT_SHOULDER.lower(): .1,
                                       mtpn.RIGHT_SHOULDER.lower(): .1},
    bk.THORACIC_SPINE_TOP_T1.name: [mtpn.LEFT_SHOULDER.lower(),
                                    mtpn.RIGHT_SHOULDER.lower()],
    bk.THORACIC_SPINE_ORIGIN_T12.name: [mtpn.LEFT_HIP.lower(),
                                        mtpn.RIGHT_HIP.lower(),
                                        mtpn.LEFT_SHOULDER.lower(),
                                        mtpn.RIGHT_SHOULDER.lower()],
    bk.PELVIS_LUMBAR_TOP_L1.name: {mtpn.LEFT_HIP.lower(): .24,
                                   mtpn.RIGHT_HIP.lower(): .24,
                                   mtpn.LEFT_SHOULDER.lower(): .26,
                                   mtpn.RIGHT_SHOULDER.lower(): .26},
    bk.PELVIS_ORIGIN.name: [mtpn.LEFT_HIP.lower(),
                            mtpn.RIGHT_HIP.lower()],
    bk.RIGHT_CLAVICLE.name: {mtpn.RIGHT_SHOULDER.lower(): .55,
                             mtpn.LEFT_SHOULDER.lower(): .45},
    bk.RIGHT_SHOULDER.name: [mtpn.RIGHT_SHOULDER.lower()],
    bk.RIGHT_ELBOW.name: [mtpn.RIGHT_ELBOW.lower()],
    bk.RIGHT_WRIST.name: [mtpn.RIGHT_WRIST.lower()],
    bk.RIGHT_INDEX_KNUCKLE.name: [mtpn.RIGHT_INDEX.lower()],
    bk.RIGHT_PINKY_KNUCKLE.name: [mtpn.RIGHT_PINKY.lower()],
    bk.RIGHT_THUMB_KNUCKLE.name: [mtpn.RIGHT_THUMB.lower()],
    bk.RIGHT_PELVIS_HIP_ACETABULUM.name: [mtpn.RIGHT_HIP.lower()],
    bk.RIGHT_KNEE.name: [mtpn.RIGHT_KNEE.lower()],
    bk.RIGHT_ANKLE.name: [mtpn.RIGHT_ANKLE.lower()],
    bk.RIGHT_HEEL.name: [mtpn.RIGHT_HEEL.lower()],
    bk.RIGHT_HALLUX_TIP.name: [mtpn.RIGHT_FOOT_INDEX.lower()],
    bk.LEFT_CLAVICLE.name: {mtpn.LEFT_SHOULDER.lower(): .55,
                            mtpn.RIGHT_SHOULDER.lower(): .45},
    bk.LEFT_SHOULDER.name: [mtpn.LEFT_SHOULDER.lower()],
    bk.LEFT_ELBOW.name: [mtpn.LEFT_ELBOW.lower()],
    bk.LEFT_WRIST.name: [mtpn.LEFT_WRIST.lower()],
    bk.LEFT_INDEX_KNUCKLE.name: [mtpn.LEFT_INDEX.lower()],
    bk.LEFT_PINKY_KNUCKLE.name: [mtpn.LEFT_PINKY.lower()],
    bk.LEFT_THUMB_KNUCKLE.name: [mtpn.LEFT_THUMB.lower()],
    bk.LEFT_PELVIS_HIP_ACETABULUM.name: [mtpn.LEFT_HIP.lower()],
    bk.LEFT_KNEE.name: [mtpn.LEFT_KNEE.lower()],
    bk.LEFT_ANKLE.name: [mtpn.LEFT_ANKLE.lower()],
    bk.LEFT_HEEL.name: [mtpn.LEFT_HEEL.lower()],
    bk.LEFT_HALLUX_TIP.name: [mtpn.LEFT_FOOT_INDEX.lower()],
}
MediapipeBodyMapping = KeypointMappingsEnum('MediapipeBodyMapping', _MEDIAPIPE_BODY_MAPPING)

if __name__ == "__main__":
    print(f"MediapipeBodyMapping enum created successfully with {len(MediapipeBodyMapping.__members__)} keys\n")
    print("\n".join([f"{key}: {value.value}" for key, value in MediapipeBodyMapping.__members__.items()]))
