from skelly_blender.core.blender_stuff.blenderizable_enum import BlenderizableEnum


class BodyKeypoints(BlenderizableEnum):
    ## skull
    SKULL_ORIGIN_FORAMEN_MAGNUM = "Gemoetric center of the foramen magnum, the hole at the base of the skull where the spinal cord enters"
    SKULL_TOP_BREGMA = "tippy top of the head, intersection of coronal and sagittal sutures"

    ### face
    SKULL_FORWARD_NOSE_TIP = "Tip of the nose"
    #### right-face
    RIGHT_SKULL_EYE_INNER = "Inner corner of the right eye socket, in the Lacrimal fossa (aka tear duct), intersection of the frontal bone and the maxilla"
    RIGHT_SKULL_EYE_CENTER = "Geometric center of the `inner` and `outer` keypoints of the right eye keypoints - NOTE - not the center of the orbit"
    RIGHT_SKULL_EYE_OUTER = "Outer corner of the right eye, intersection of the frontal bone and the zygomatic bone"
    RIGHT_SKULL_ACOUSTIC_MEATUS = "Entrance to the Right ear canal, intersection of the temporal bone and the mandible (behind tragus)"
    RIGHT_SKULL_CANINE_TOOTH_TIP = "Tip of the right canine tooth, roughly behind the right corner of the mouth"
    #### left-face,
    LEFT_SKULL_EYE_INNER ="Inner corner of the left eye socket, in the Lacrimal fossa (aka tear duct), intersection of the frontal bone and the maxilla"
    LEFT_SKULL_EYE_CENTER ="Geometric center of the `inner` and `outer` keypoints of the left eye keypoints - NOTE - not the center of the orbit"
    LEFT_SKULL_EYE_OUTER ="Outer corner of the left eye, intersection of the frontal bone and the zygomatic bone"
    LEFT_SKULL_ACOUSTIC_MEATUS ="Entrance to the Right ear canal, intersection of the temporal bone and the mandible (behind tragus)"
    LEFT_SKULL_CANINE_TOOTH_TIP ="Tip of the left canine tooth, roughly behind the right corner of the mouth"


    ## axial skeleton
    ## neck,
    CERVICAL_SPINE_TOP_C1_AXIS = "Top of the neck segment, the geometric center of the top surface of the second cervical vertebra (C2) aka the `Axis`"
    CERVICAL_SPINE_ORIGIN_C7 = "Base of the neck, geometric center of the bottom surface of the seventh cervical vertebra (C7)"

    ## chest,
    THORACIC_SPINE_TOP_T1 = "Geometric center of the top surface of the first thoracic vertebra (T1)"
    THORACIC_SPINE_ORIGIN_T12 = "Geometric center of the bottom surface of the twelfth thoracic vertebra (T12)"
    STERNUM_TOP_SUPRASTERNAL_NOTCH = "Geometric center of the suprasternal notch, the dip at the top of the sternum"
    STERNUM_ORIGIN_XIPHOID_PROCESS = "Geometric center of the xiphoid process, the bottom tip of the sternum"


    ## pelvis,
    PELVIS_ORIGIN = "Geometric center of the left and right hip sockets, anterior to the Sacrum"
    PELVIS_LUMBAR_TOP_L1 = "Geometric center of the top surface of the first lumbar vertebra (L1)"
    RIGHT_PELVIS_HIP_ACETABULUM = "Geometric center of proximal surface the right hip socket/acetabulum (where the femoral head fits in)"
    LEFT_PELVIS_HIP_ACETABULUM = "Geometric center of proximal surface the left hip socket/acetabulum (where the femoral head fits in)"

    ### right arm
    RIGHT_CLAVICLE = "Center of the right sternoclavicular joint"
    RIGHT_SHOULDER = "Center of the right glenohumeral joint"
    RIGHT_ELBOW = "Center of the right elbow joint, near trochlea of the humerus"
    RIGHT_WRIST = "Center of the right radiocarpal joint, near the lunate fossa of the radius"


    ### right (mitten) hand
    RIGHT_THUMB_KNUCKLE = "Center of the metacarpophalangeal joint of the right thumb"
    RIGHT_INDEX_KNUCKLE = "Center of the metacarpophalangeal joint of the right index finger"
    RIGHT_MIDDLE_KNUCKLE = "Center of the metacarpophalangeal joint of the right index finger"
    RIGHT_RING_KNUCKLE = "Center of the metacarpophalangeal joint of the right index finger"
    RIGHT_PINKY_KNUCKLE = "Center of the metacarpophalangeal joint of the right pinky finger"

    ### right leg
    RIGHT_KNEE = "Center of the right knee joint, intersection of the medial condyle of the femur and the tibia"
    RIGHT_ANKLE = "Center of the right ankle joint, geometric center of the medial and lateral malleoli"
    RIGHT_HEEL = "Contact surface of the right heel with the ground, most distal point of the calcaneus"
    RIGHT_HALLUX_TIP = "Tippy tip of right hallux, aka the big toe"

    ### left arm
    LEFT_CLAVICLE = "Center of the left sternoclavicular joint"
    LEFT_SHOULDER = "Center of the left glenohumeral joint"
    LEFT_ELBOW = "Center of the left elbow joint, near trochlea of the humerus"
    LEFT_WRIST = "Center of the left radiocarpal joint, near the lunate fossa of the radius"


    ### left (mitten) hand
    LEFT_THUMB_KNUCKLE = "Center of the left metacarpophalangeal joint of the thumb"
    LEFT_INDEX_KNUCKLE = "Center of the left metacarpophalangeal joint of the index finger"
    LEFT_MIDDLE_KNUCKLE = "Center of the left metacarpophalangeal joint of the index finger"
    LEFT_RING_KNUCKLE = "Center of the left metacarpophalangeal joint of the index finger"
    LEFT_PINKY_KNUCKLE = "Center of the left metacarpophalangeal joint of the pinky finger"


    ### left leg
    LEFT_KNEE = "Center of the left knee joint, intersection of the medial condyle of the femur and the tibia"
    LEFT_ANKLE = "Center of the left ankle joint, geometric center of the medial and lateral malleoli"
    LEFT_HEEL = "Contact surface of the left heel with the ground, most distal point of the calcaneus"
    LEFT_HALLUX_TIP = "Tippy tip of the left hallux, aka the big toe"



# Example usage
if __name__ == "__main__":
    print("\n".join([f"{key}: {value.value}" for key, value in BodyKeypoints.__members__.items()]))

    print("Blenderized names:")
    print("\n".join([value.blenderize() for value in BodyKeypoints.__members__.values()]))
