from enum import Enum
from typing import List, Dict

from freemocap_blender_addon.models.animation.armatures.bones.bone_constraint_types import ConstraintABC, \
    BoneConstraintTypes, TrackAxis, OwnerSpace, LockAxis
from skelly_blender.core.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import AxialSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import SkullSegments

# Enums for specific keys to avoid spelling issues

_BODY_BONE_CONSTRAINTS: Dict[str, List[ConstraintABC]] = {
    # AXIAL SEGMENTS
    # Spine
    AxialSegments.PELVIS_LUMBAR.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_ORIGIN.blenderize()),
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
    AxialSegments.THORACIC_SPINE.blenderize(): [
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
    AxialSegments.CERVICAL_SPINE.blenderize(): [
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
    SkullSegments.NOSE.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.SKULL_FORWARD_NOSE_TIP.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    # RIGHT FACE
    SkullSegments.RIGHT_EYE_INNER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_EYE_INNER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.RIGHT_EYE_CENTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_EYE_CENTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.RIGHT_EYE_OUTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_EYE_OUTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.RIGHT_EAR_TRAGUS.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.RIGHT_MOUTH.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    # LEFT FACE
    SkullSegments.LEFT_EYE_INNER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_EYE_INNER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.LEFT_EYE_CENTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_EYE_CENTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.LEFT_EYE_OUTER.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_EYE_OUTER.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.LEFT_EAR_TRAGUS.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    SkullSegments.LEFT_MOUTH.blenderize():
        [BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP.blenderize(),
                                                track_axis=TrackAxis.TRACK_Y.value)],

    # RIGHT BODY SEGMENTS
    # RIGHT UPPER LIMB
    RightBodySegments.RIGHT_CLAVICLE.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_SHOULDER.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value), ],
    RightBodySegments.RIGHT_UPPER_ARM.blenderize(): [
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
    RightBodySegments.RIGHT_FOREARM.blenderize(): [
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
    RightBodySegments.RIGHT_WRIST_INDEX.blenderize(): [
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

    RightBodySegments.RIGHT_WRIST_PINKY.blenderize(): [
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
    RightBodySegments.RIGHT_WRIST_THUMB.blenderize(): [
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
    RightBodySegments.RIGHT_PELVIS.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_ORIGIN.blenderize()),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Z.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

    RightBodySegments.RIGHT_THIGH.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM.blenderize()),
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
    RightBodySegments.RIGHT_CALF.blenderize(): [
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

    RightBodySegments.RIGHT_FORE_FOOT.blenderize(): [
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

    RightBodySegments.RIGHT_HEEL.blenderize(): [
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.RIGHT_HEEL.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

    # LEFT BODY SEGMENTS
    # LEFT UPPER LIMB
    LeftBodySegments.LEFT_CLAVICLE.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7.blenderize()),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_SHOULDER.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value), ],
    LeftBodySegments.LEFT_UPPER_ARM.blenderize(): [
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
    LeftBodySegments.LEFT_FOREARM.blenderize(): [
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
    LeftBodySegments.LEFT_WRIST_INDEX.blenderize(): [
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
    LeftBodySegments.LEFT_WRIST_PINKY.blenderize(): [
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
    LeftBodySegments.LEFT_WRIST_THUMB.blenderize(): [
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
    LeftBodySegments.LEFT_PELVIS.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.PELVIS_ORIGIN.blenderize()),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.LEFT_PELVIS_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Z.value,
            influence=1.0,
        ),
        BoneConstraintTypes.LOCKED_TRACK.value(
            target=BodyKeypoints.LEFT_PELVIS_HIP_ACETABULUM.blenderize(),
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        BoneConstraintTypes.DAMPED_TRACK.value(target=BodyKeypoints.LEFT_PELVIS_HIP_ACETABULUM.blenderize(),
                                               track_axis=TrackAxis.TRACK_Y.value)

    ],

    LeftBodySegments.LEFT_THIGH.blenderize(): [
        BoneConstraintTypes.COPY_LOCATION.value(target=BodyKeypoints.LEFT_PELVIS_HIP_ACETABULUM.blenderize()),
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

    LeftBodySegments.LEFT_CALF.blenderize(): [
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

    LeftBodySegments.LEFT_FORE_FOOT.blenderize(): [
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

    LeftBodySegments.LEFT_HEEL.blenderize(): [
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
