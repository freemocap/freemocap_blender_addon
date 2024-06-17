from enum import Enum
from typing import List, Dict

from freemocap_blender_addon.models.animation.armatures.bones.bone_constraint_types import TrackAxis, LockAxis, OwnerSpace, \
    Constraint, CopyLocationConstraint, LockedTrackConstraint, DampedTrackConstraint, LimitRotationConstraint
from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BlenderizedKeypointNames as bkn
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import BlenderizedAxialSegments as bas
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import BlenderizedLeftBodySegments as blbs
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import BlenderizedRightBodySegments as brbs
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import BlenderizedSkullSegments

# Enums for specific keys to avoid spelling issues

_BODY_BONE_CONSTRAINTS: Dict[str, List[Constraint]] = {
    # AXIAL SEGMENTS
    # Spine
    bas.LUMBAR_SPINE.value: [
        CopyLocationConstraint(target=bkn.PELVIS_CENTER.value),
        DampedTrackConstraint(target=bkn.CHEST_CENTER_T12.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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
    bas.THORACIC_SPINE.value: [
        DampedTrackConstraint(target=bkn.NECK_BASE_C7.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LockedTrackConstraint(
            target=bkn.RIGHT_SHOULDER,
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        LimitRotationConstraint(
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
    bas.CERVICAL_SPINE.value: [
        DampedTrackConstraint(target=bkn.SKULL_CENTER_ATLAS_C1.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LockedTrackConstraint(
            target=bkn.NOSE_TIP.value,
            track_axis=TrackAxis.TRACK_Z.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        LimitRotationConstraint(
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
    BlenderizedSkullSegments.NOSE.value:
        [DampedTrackConstraint(target=bkn.NOSE_TIP.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    # RIGHT FACE
    BlenderizedSkullSegments.RIGHT_EYE_INNER.value:
        [DampedTrackConstraint(target=bkn.RIGHT_EYE_INNER.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.RIGHT_EYE_CENTER.value:
        [DampedTrackConstraint(target=bkn.RIGHT_EYE_CENTER.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.RIGHT_EYE_OUTER.value:
        [DampedTrackConstraint(target=bkn.RIGHT_EYE_OUTER.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.RIGHT_EAR_TRAGUS.value:
        [DampedTrackConstraint(target=bkn.RIGHT_EAR_TRAGUS.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.RIGHT_MOUTH.value:
        [DampedTrackConstraint(target=bkn.RIGHT_MOUTH.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    # LEFT FACE
    BlenderizedSkullSegments.LEFT_EYE_INNER.value:
        [DampedTrackConstraint(target=bkn.LEFT_EYE_INNER.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.LEFT_EYE_CENTER.value:
        [DampedTrackConstraint(target=bkn.LEFT_EYE_CENTER.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.LEFT_EYE_OUTER.value:
        [DampedTrackConstraint(target=bkn.LEFT_EYE_OUTER.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.LEFT_EAR_TRAGUS.value:
        [DampedTrackConstraint(target=bkn.LEFT_EAR_TRAGUS.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    BlenderizedSkullSegments.LEFT_MOUTH.value:
        [DampedTrackConstraint(target=bkn.LEFT_MOUTH.value,
                               track_axis=TrackAxis.TRACK_Y.value)],

    # RIGHT BODY SEGMENTS
    # RIGHT UPPER LIMB
    brbs.RIGHT_CLAVICLE.value: [
        CopyLocationConstraint(target=bkn.NECK_BASE_C7.value),
        DampedTrackConstraint(target=bkn.RIGHT_SHOULDER.value,
                              track_axis=TrackAxis.TRACK_Y.value), ],
    brbs.RIGHT_UPPER_ARM.value: [
        DampedTrackConstraint(target=bkn.RIGHT_ELBOW.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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
    brbs.RIGHT_FOREARM.value: [
        DampedTrackConstraint(target=bkn.RIGHT_WRIST.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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
    brbs.RIGHT_WRIST_INDEX.value: [
        DampedTrackConstraint(target=bkn.RIGHT_INDEX_KNUCKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LockedTrackConstraint(
            target=bkn.RIGHT_THUMB_KNUCKLE.value,  # originally -> "right_hand_thumb_cmc",
            track_axis=TrackAxis.TRACK_Z.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        LimitRotationConstraint(
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
    brbs.RIGHT_WRIST_PINKY.value: [
        DampedTrackConstraint(target=bkn.RIGHT_PINKY_KNUCKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LockedTrackConstraint(
            target=bkn.RIGHT_THUMB_KNUCKLE.value,  # originally - "right_hand_thumb_cmc",
            track_axis=TrackAxis.TRACK_Z.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        LimitRotationConstraint(
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
    brbs.RIGHT_WRIST_THUMB.value: [
        DampedTrackConstraint(target=bkn.RIGHT_THUMB_KNUCKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        # TODO - revisit when we add the detailed hand
        # LockedTrackConstraint(
        #     target="right_hand_thumb_cmc",
        #     track_axis=TrackAxis.TRACK_Z.value,
        #     lock_axis=LockAxis.LOCK_Y.value,
        #     influence=1.0,
        # ),
        LimitRotationConstraint(
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
    brbs.RIGHT_PELVIS.value: [
        CopyLocationConstraint(target=bkn.PELVIS_CENTER.value),
        LockedTrackConstraint(
            target=bkn.RIGHT_HIP.value,
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Z,
            influence=1.0,
        ),
        LockedTrackConstraint(
            target=bkn.RIGHT_HIP.value,
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        DampedTrackConstraint(target=bkn.RIGHT_HIP.value,
                              track_axis=TrackAxis.TRACK_Y.value)

    ],

    brbs.RIGHT_THIGH.value: [
        CopyLocationConstraint(target=bkn.RIGHT_HIP.value),
        DampedTrackConstraint(target=bkn.RIGHT_KNEE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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
    brbs.RIGHT_CALF.value: [
        DampedTrackConstraint(target=bkn.RIGHT_ANKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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

    brbs.RIGHT_FORE_FOOT.value: [
        DampedTrackConstraint(target=bkn.RIGHT_HALLUX_TIP,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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

    brbs.RIGHT_HEEL.value: [
        DampedTrackConstraint(target=bkn.RIGHT_HEEL.value,
                              track_axis=TrackAxis.TRACK_Y.value)

    ],

    # LEFT BODY SEGMENTS
    # LEFT UPPER LIMB
    blbs.LEFT_CLAVICLE.value: [
        CopyLocationConstraint(target=bkn.NECK_BASE_C7.value),
        DampedTrackConstraint(target=bkn.LEFT_SHOULDER.value,
                              track_axis=TrackAxis.TRACK_Y.value), ],
    blbs.LEFT_UPPER_ARM.value: [
        DampedTrackConstraint(target=bkn.LEFT_ELBOW.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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
    blbs.LEFT_FOREARM.value: [
        DampedTrackConstraint(target=bkn.LEFT_WRIST.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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
    blbs.LEFT_WRIST_INDEX.value: [
        DampedTrackConstraint(target=bkn.LEFT_INDEX_KNUCKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LockedTrackConstraint(
            target=bkn.LEFT_THUMB_KNUCKLE.value,  # originally -> "right_hand_thumb_cmc",
            track_axis=TrackAxis.TRACK_Z.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        LimitRotationConstraint(
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
    blbs.LEFT_WRIST_PINKY.value: [
        DampedTrackConstraint(target=bkn.LEFT_PINKY_KNUCKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LockedTrackConstraint(
            target=bkn.LEFT_THUMB_KNUCKLE.value,  # originally - "right_hand_thumb_cmc",
            track_axis=TrackAxis.TRACK_Z.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        LimitRotationConstraint(
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
    blbs.LEFT_WRIST_THUMB.value: [
        DampedTrackConstraint(target=bkn.LEFT_THUMB_KNUCKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        # TODO - revisit when we add the detailed hand
        # LockedTrackConstraint(
        #     target="right_hand_thumb_cmc",
        #     track_axis=TrackAxis.TRACK_Z.value,
        #     lock_axis=LockAxis.LOCK_Y.value,
        #     influence=1.0,
        # ),
        LimitRotationConstraint(
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
    blbs.LEFT_PELVIS.value: [
        CopyLocationConstraint(target=bkn.PELVIS_CENTER.value),
        LockedTrackConstraint(
            target=bkn.LEFT_HIP.value,
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Z,
            influence=1.0,
        ),
        LockedTrackConstraint(
            target=bkn.LEFT_HIP.value,
            track_axis=TrackAxis.TRACK_NEGATIVE_X.value,
            lock_axis=LockAxis.LOCK_Y.value,
            influence=1.0,
        ),
        DampedTrackConstraint(target=bkn.LEFT_HIP.value,
                              track_axis=TrackAxis.TRACK_Y.value)

    ],



    blbs.LEFT_THIGH.value: [
        CopyLocationConstraint(target=bkn.LEFT_HIP.value),
        DampedTrackConstraint(target=bkn.LEFT_KNEE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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

    blbs.LEFT_CALF.value: [
        DampedTrackConstraint(target=bkn.LEFT_ANKLE.value,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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

    blbs.LEFT_FORE_FOOT.value: [
        DampedTrackConstraint(target=bkn.LEFT_HALLUX_TIP,
                              track_axis=TrackAxis.TRACK_Y.value),

        LimitRotationConstraint(
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

    blbs.LEFT_HEEL.value: [
        DampedTrackConstraint(target=bkn.LEFT_HEEL.value,
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
#     DampedTrackConstraint(
#         target="right_hand_thumb_cmc",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.01.R": [
#     DampedTrackConstraint(
#         target="right_hand_thumb_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.02.R": [
#     DampedTrackConstraint(
#         target="right_hand_thumb_ip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.03.R": [
#     DampedTrackConstraint(
#         target="right_hand_thumb_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.01.R": [
#     DampedTrackConstraint(
#         target="right_hand_index_finger_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.01.R": [
#     DampedTrackConstraint(
#         target="right_hand_index_finger_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.02.R": [
#     DampedTrackConstraint(
#         target="right_hand_index_finger_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.03.R": [
#     DampedTrackConstraint(
#         target="right_hand_index_finger_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.02.R": [
#     DampedTrackConstraint(
#         target="right_hand_middle_finger_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.01.R": [
#     DampedTrackConstraint(
#         target="right_hand_middle_finger_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.02.R": [
#     DampedTrackConstraint(
#         target="right_hand_middle_finger_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.03.R": [
#     DampedTrackConstraint(
#         target="right_hand_middle_finger_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.03.R": [
#     DampedTrackConstraint(
#         target="right_hand_ring_finger_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.01.R": [
#     DampedTrackConstraint(
#         target="right_hand_ring_finger_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.02.R": [
#     DampedTrackConstraint(
#         target="right_hand_ring_finger_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.03.R": [
#     DampedTrackConstraint(
#         target="right_hand_ring_finger_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.04.R": [
#     DampedTrackConstraint(
#         target="right_hand_pinky_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.01.R": [
#     DampedTrackConstraint(
#         target="right_hand_pinky_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.02.R": [
#     DampedTrackConstraint(
#         target="right_hand_pinky_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.03.R": [
#     DampedTrackConstraint(
#         target="right_hand_pinky_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.carpal.L": [
#     DampedTrackConstraint(
#         target="left_hand_thumb_cmc",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.01.L": [
#     DampedTrackConstraint(
#         target="left_hand_thumb_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "thumb.02.L": [
#     DampedTrackConstraint(target="left_hand_thumb_ip",
#     track_axis=TrackAxis.TRACK_Y.value)

# ],
# "thumb.03.L": [
#     DampedTrackConstraint(
#         target="left_hand_thumb_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.01.L": [
#     DampedTrackConstraint(
#         target="left_hand_index_finger_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.01.L": [
#     DampedTrackConstraint(
#         target="left_hand_index_finger_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.02.L": [
#     DampedTrackConstraint(
#         target="left_hand_index_finger_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_index.03.L": [
#     DampedTrackConstraint(
#         target="left_hand_index_finger_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.02.L": [
#     DampedTrackConstraint(
#         target="left_hand_middle_finger_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.01.L": [
#     DampedTrackConstraint(
#         target="left_hand_middle_finger_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.02.L": [
#     DampedTrackConstraint(
#         target="left_hand_middle_finger_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_middle.03.L": [
#     DampedTrackConstraint(
#         target="left_hand_middle_finger_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.03.L": [
#     DampedTrackConstraint(
#         target="left_hand_ring_finger_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.01.L": [
#     DampedTrackConstraint(
#         target="left_hand_ring_finger_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.02.L": [
#     DampedTrackConstraint(
#         target="left_hand_ring_finger_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_ring.03.L": [
#     DampedTrackConstraint(
#         target="left_hand_ring_finger_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "palm.04.L": [
#     DampedTrackConstraint(
#         target="left_hand_pinky_mcp",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.01.L": [
#     DampedTrackConstraint(
#         target="left_hand_pinky_pip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.02.L": [
#     DampedTrackConstraint(
#         target="left_hand_pinky_dip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
# "f_pinky.03.L": [
#     DampedTrackConstraint(
#         target="left_hand_pinky_tip",
#         track_axis=TrackAxis.TRACK_Y.value

#     )
# ],
