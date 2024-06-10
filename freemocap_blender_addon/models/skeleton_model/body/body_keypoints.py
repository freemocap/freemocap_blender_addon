from enum import StrEnum


class SkullKeypoints(StrEnum):
    ## head
    SKULL_CENTER_ATLAS_C1 = "Center of the skull volume (like, rotational center, not necessarily the center of mass)",

    ### face
    # SKULL_TOP_BREGMA = "tippy top of the head, intersection of coronal and sagittal sutures",
    NOSE_TIP = "Tip of the nose",
    #### right-face
    RIGHT_EYE_INNER = "Inner corner of the right eye, the tear duct, intersection of the frontal bone and the maxilla",
    RIGHT_EYE_CENTER = "Geometric center of the `inner` and `outer` eye keypoints - NOTE - not the center of the orbit",
    RIGHT_EYE_OUTER = "Outer corner of the right eye, intersection of the frontal bone and the zygomatic bone",
    RIGHT_EAR_TRAGUS = "The little nubbin on the front of the ear,  intersection of the temporal bone and the mandible",
    RIGHT_MOUTH = "outer corner of the mouth",
    #### left-face,
    LEFT_EYE_INNER = "Inner corner of the left eye, the tear duct, intersection of the frontal bone and the maxilla",
    LEFT_EYE_CENTER = "Geometric center of the `inner` and `outer` eye keypoints - NOTE - not the center of the orbit",
    LEFT_EYE_OUTER = "Outer corner of the left eye, intersection of the frontal bone and the zygomatic bone",
    LEFT_EAR_TRAGUS = "The little nubbin on the front of the ear, intersection of the temporal bone and the mandible",
    LEFT_MOUTH = "outer corner of the mouth",


class AxialSkeletonKeypoints(StrEnum):
    ## neck,
    NECK_TOP_AXIS_C2 = "Top of the neck segment, the geometric center of the top surface of the second cervical vertebra (C2) aka the `Axis`",
    NECK_BASE_C7 = "Base of the neck, geometric center of the bottom surface of the seventh cervical vertebra (C7)",

    ## chest,
    CHEST_CENTER_T12 = "Geometric center of the top surface of the first thoracic vertebra (T1)",

    ## root,
    PELVIS_CENTER = "Geometric center of the left and right hip sockets, anterior to the Sacrum",


class RightArmKeypoints(StrEnum):
    ### right arm
    RIGHT_CLAVICLE = "Center of the right sternoclavicular joint",
    RIGHT_SHOULDER = "Center of the right glenohumeral joint",
    RIGHT_ELBOW = "Center of the right elbow joint, near trochlea of the humerus",
    RIGHT_WRIST = "Center of the right radiocarpal joint, near the lunate fossa of the radius",


class RightMittenHandKeypoints(StrEnum):
    ### right (mitten) hand
    RIGHT_THUMB_KNUCKLE = "Center of the metacarpophalangeal joint of the right thumb",
    RIGHT_INDEX_KNUCKLE = "Center of the metacarpophalangeal joint of the right index finger",
    RIGHT_MIDDLE_KNUCKLE = "Center of the metacarpophalangeal joint of the right index finger",
    RIGHT_RING_KNUCKLE = "Center of the metacarpophalangeal joint of the right index finger",
    RIGHT_PINKY_KNUCKLE = "Center of the metacarpophalangeal joint of the right pinky finger",


class RightLegKeypoints(StrEnum):
    RIGHT_HIP = "Geometric center of the right hip socket/acetabulum/femoral head",
    RIGHT_KNEE = "Center of the right knee joint, intersection of the medial condyle of the femur and the tibia",
    RIGHT_ANKLE = "Center of the right ankle joint, geometric center of the medial and lateral malleoli",
    RIGHT_HEEL = "Contact surface of the right heel with the ground, most distal point of the calcaneus",
    RIGHT_HALLUX_TIP = "Tippy tip of right hallux, aka the big toe",


class LeftArmKeypoints(StrEnum):
    LEFT_CLAVICLE = "Center of the left sternoclavicular joint",
    LEFT_SHOULDER = "Center of the left glenohumeral joint",
    LEFT_ELBOW = "Center of the left elbow joint, near trochlea of the humerus",
    LEFT_WRIST = "Center of the left radiocarpal joint, near the lunate fossa of the radius",


class LeftMittenHandKeypoints(StrEnum):
    LEFT_THUMB_KNUCKLE = "Center of the left metacarpophalangeal joint of the thumb",
    LEFT_INDEX_KNUCKLE = "Center of the left metacarpophalangeal joint of the index finger",
    LEFT_MIDDLE_KNUCKLE = "Center of the left metacarpophalangeal joint of the index finger",
    LEFT_RING_KNUCKLE = "Center of the left metacarpophalangeal joint of the index finger",
    LEFT_PINKY_KNUCKLE = "Center of the left metacarpophalangeal joint of the pinky finger",


class LeftLegKeypoints(StrEnum):
    LEFT_HIP = "Geometric center of the left hip socket/acetabulum/femoral head",
    LEFT_KNEE = "Center of the left knee joint, intersection of the medial condyle of the femur and the tibia",
    LEFT_ANKLE = "Center of the left ankle joint, geometric center of the medial and lateral malleoli",
    LEFT_HEEL = "Contact surface of the left heel with the ground, most distal point of the calcaneus",
    LEFT_HALLUX_TIP = "Tippy tip of the left hallux, aka the big toe",


def combine_enums(*enum_classes):
    combined = {}
    for enum_class in enum_classes:
        for name, member in enum_class.__members__.items():
            if name in combined:
                raise ValueError(f"Duplicate enum member name found: {name}")
            combined[name] = member.value
    return combined


combined_keypoints = combine_enums(
    SkullKeypoints,
    AxialSkeletonKeypoints,
    RightArmKeypoints,
    RightMittenHandKeypoints,
    RightLegKeypoints,
    LeftArmKeypoints,
    LeftMittenHandKeypoints,
    LeftLegKeypoints
)

BodyKeypoints = StrEnum('BodyKeypoints', combined_keypoints)

# Example usage
if __name__ == "__main__":
    print("\n".join([f"{kp.name}: {kp.value}" for kp in list(BodyKeypoints)]))
