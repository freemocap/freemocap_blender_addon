from enum import Enum
from typing import List, Dict

from skelly_blender.core.needs_bpy.armature_rig.bone_constraints.bone_constraint_types import ConstraintABC, \
    BoneConstraintTypes, TrackAxis, OwnerSpace, LockAxis
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_segments import \
    BodySegments


_BODY_BONE_CONSTRAINTS: Dict[str, List[ConstraintABC]] = {
    # AXIAL SEGMENTS
    # Spine
    BodySegments.PELVIS_LUMBAR.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_LUMBAR_ORIGIN.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.PELVIS_LUMBAR_TOP_L1.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=68,
            use_limit_y=True,
            min_y=-45,
            max_y=45,
            use_limit_z=True,
            min_z=-30,
            max_z=30,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.SPINE_THORACIC.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.RIGHT_SHOULDER.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=22,
            use_limit_y=True,
            min_y=-45,
            max_y=45,
            use_limit_z=True,
            min_z=-30,
            max_z=30,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.SPINE_CERVICAL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.SKULL_FORWARD_NOSE_TIP.blenderize(),
            track_axis=TrackAxis.TRACK_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-37,
            max_x=22,
            use_limit_y=True,
            min_y=-45,
            max_y=45,
            use_limit_z=True,
            min_z=-30,
            max_z=30,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],

    # SKULL
    BodySegments.SKULL_NOSE.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.SKULL_FORWARD_NOSE_TIP.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    # RIGHT FACE
    BodySegments.SKULL_RIGHT_EYE_INNER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_EYE_INNER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_RIGHT_EYE_CENTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_EYE_CENTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_RIGHT_EYE_OUTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_EYE_OUTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_RIGHT_EAR.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_RIGHT_MOUTH.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    # LEFT FACE
    BodySegments.SKULL_LEFT_EYE_INNER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_EYE_INNER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_LEFT_EYE_CENTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_EYE_CENTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_LEFT_EYE_OUTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_EYE_OUTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_LEFT_EAR.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    BodySegments.SKULL_LEFT_MOUTH.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    # RIGHT BODY SEGMENTS
    # RIGHT UPPER LIMB
    BodySegments.RIGHT_CLAVICLE.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SHOULDER.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value), ],
    BodySegments.RIGHT_ARM_PROXIMAL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_ELBOW.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-135,
            max_x=90,
            use_limit_y=True,
            min_y=-98,
            max_y=180,
            use_limit_z=True,
            min_z=-97,
            max_z=91,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.RIGHT_ARM_DISTAL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_WRIST.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-90,
            max_x=79,
            use_limit_y=True,
            min_y=0,
            max_y=146,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.RIGHT_PALM_PINKY.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_INDEX_KNUCKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.RIGHT_THUMB_KNUCKLE.value,  # originally -> "right_hand_thumbblenderize(),
            track_axis=TrackAxis.TRACK_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL.value,
        ),

    ],

    BodySegments.RIGHT_PALM_PINKY.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_PINKY_KNUCKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.RIGHT_THUMB_KNUCKLE.value,  # originally - "right_hand_thumbblenderize(),
            track_axis=TrackAxis.TRACK_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL.value,
        ),

    ],
    BodySegments.RIGHT_PALM_PINKY.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_THUMB_KNUCKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        # TODO - revisit when we add the detailed hand
        # BoneConstraintTypes.LOCKED_TRACK.value(
        #     target="right_hand_thumbblenderize(),
        #     track_axis=TrackAxis.TRACK_X.value,
        #     lock_axis=LockAxis.LOCK_Y.value,
        #     influence=1.0,
        # ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL.value,
        ),

    ],
    ## RIGHT LOWER LIMB
    BodySegments.PELVIS_RIGHT.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_LUMBAR_ORIGIN.blenderize()),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Z.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

    BodySegments.RIGHT_LEG_THIGH.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_KNEE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-155,
            max_x=45,
            use_limit_y=True,
            min_y=-105,
            max_y=85,
            use_limit_z=True,
            min_z=-88,
            max_z=17,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.RIGHT_LEG_CALF.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_ANKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=0,
            max_x=150,
            use_limit_y=True,
            min_y=0,
            max_y=0,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],

    BodySegments.RIGHT_FOOT_FRONT.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_HALLUX_TIP.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-31,
            max_x=63,
            use_limit_y=True,
            min_y=-26,
            max_y=26,
            use_limit_z=True,
            min_z=-15,
            max_z=74,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],

    BodySegments.RIGHT_FOOT_HEEL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_HEEL.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

    # LEFT BODY SEGMENTS
    # LEFT UPPER LIMB
    BodySegments.LEFT_CLAVICLE.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SHOULDER.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value), ],
    BodySegments.LEFT_ARM_PROXIMAL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_ELBOW.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-135,
            max_x=90,
            use_limit_y=True,
            min_y=-98,
            max_y=180,
            use_limit_z=True,
            min_z=-97,
            max_z=91,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.LEFT_ARM_DISTAL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_WRIST.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-90,
            max_x=79,
            use_limit_y=True,
            min_y=0,
            max_y=146,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],
    BodySegments.LEFT_PALM_INDEX.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_INDEX_KNUCKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.LEFT_THUMB_KNUCKLE.value,  # originally -> "right_hand_thumbblenderize(),
            track_axis=TrackAxis.TRACK_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL.value,
        ),

    ],
    BodySegments.LEFT_PALM_PINKY.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_PINKY_KNUCKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.LEFT_THUMB_KNUCKLE.value,  # originally - "right_hand_thumbblenderize(),
            track_axis=TrackAxis.TRACK_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL.value,
        ),

    ],
    BodySegments.LEFT_PALM_THUMB.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_THUMB_KNUCKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        # TODO - revisit when we add the detailed hand
        # BoneConstraintTypes.LOCKED_TRACK.value(
        #     target="right_hand_thumbblenderize(),
        #     track_axis=TrackAxis.TRACK_X.value,
        #     lock_axis=LockAxis.LOCK_Y.value,
        #     influence=1.0,
        # ),
        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL.value,
        ),

    ],
    ## LEFT LOWER LIMB
    BodySegments.PELVIS_LEFT.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_LUMBAR_ORIGIN.blenderize()),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Z.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

    BodySegments.LEFT_LEG_THIGH.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_KNEE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-155,
            max_x=45,
            use_limit_y=True,
            min_y=-105,
            max_y=85,
            use_limit_z=True,
            min_z=-88,
            max_z=17,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],

    BodySegments.LEFT_LEG_CALF.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_ANKLE.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=0,
            max_x=150,
            use_limit_y=True,
            min_y=0,
            max_y=0,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],

    BodySegments.LEFT_FOOT_FRONT.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_HALLUX_TIP.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value),

        BoneConstraintTypes.LIMIT_ROTATION.value(
            use_limit_x=True,
            min_x=-31,
            max_x=63,
            use_limit_y=True,
            min_y=-26,
            max_y=26,
            use_limit_z=True,
            min_z=-15,
            max_z=74,
            owner_space=OwnerSpace.LOCAL.value,
        ),
    ],

    BodySegments.LEFT_FOOT_HEEL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_HEEL.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

}

DefaultBoneConstraints = Enum('BodyBoneConstraints', _BODY_BONE_CONSTRAINTS)

if __name__ == "__main__":
    out_string = "BodyBoneConstraints:\n"
    for name, member in DefaultBoneConstraints.__members__.items():
        out_string += f"{name}:\n"
        for constraint in member.value:
            out_string += f"\t{constraint}\n"
    print(out_string)

#
# "thumb.carpal.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_thumbblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.01.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_thumbblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.02.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_thumblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.03.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_thumbblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.01.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.01.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.02.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.03.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.02.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.01.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.02.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.03.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.03.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.01.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.02.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.03.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.04.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.01.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.02.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.03.R": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="right_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.carpal.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_thumbblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.01.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_thumbblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.02.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(target="left_hand_thumblenderize(),
#     track_axis=TrackAxis.TRACK_Y.value)

# ],
# "thumb.03.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_thumbblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.01.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.01.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.02.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.03.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_index_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.02.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.01.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.02.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.03.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_middle_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.03.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.01.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.02.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.03.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_ring_fingerblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.04.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.01.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.02.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.03.L": [
#     BoneConstraintTypes.DAMPED_TRACK.value(
#         target="left_hand_pinkyblenderize(),
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
