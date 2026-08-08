bone_naming_mapping = {
    "metahuman": {
        'pelvis': 'pelvis',
        'pelvis.R': 'pelvis_r',
        'pelvis.L': 'pelvis_l',
        'spine': 'spine_01',
        'spine.001': 'spine_04',
        'neck': 'neck_01',
        'face': 'head',
        'shoulder.R': 'clavicle_r',
        'shoulder.L': 'clavicle_l',
        'upper_arm.R': 'upperarm_r',
        'upper_arm.L': 'upperarm_l',
        'forearm.R': 'lowerarm_r',
        'forearm.L': 'lowerarm_l',
        'hand.R': 'hand_r',
        'hand.L': 'hand_l',
        'thumb.carpal.R': 'thumb_metacarpal_r',
        'palm.01.R': 'index_mcarpal_r', # Changed name so the automatic retargeting in UE does not detect this bone
        'palm.02.R': 'middle_mcarpal_r', # Changed name so the automatic retargeting in UE does not detect this bone
        'palm.03.R': 'ring_mcarpal_r', # Changed name so the automatic retargeting in UE does not detect this bone
        'palm.04.R': 'pinky_mcarpal_r', # Changed name so the automatic retargeting in UE does not detect this bone
        'thumb.carpal.L': 'thumb_metacarpal_l',
        'palm.01.L': 'index_mcarpal_l', # Changed name so the automatic retargeting in UE does not detect this bone
        'palm.02.L': 'middle_mcarpal_l', # Changed name so the automatic retargeting in UE does not detect this bone
        'palm.03.L': 'ring_mcarpal_l', # Changed name so the automatic retargeting in UE does not detect this bone
        'palm.04.L': 'pinky_mcarpal_l', # Changed name so the automatic retargeting in UE does not detect this bone
        'thumb.01.R': 'thumb_01_r',
        'thumb.01.L': 'thumb_01_l',
        'thumb.02.R': 'thumb_02_r',
        'thumb.02.L': 'thumb_02_l',
        'thumb.03.R': 'thumb_03_r',
        'thumb.03.L': 'thumb_03_l',
        'f_index.01.R': 'index_01_r',
        'f_index.01.L': 'index_01_l',
        'f_index.02.R': 'index_02_r',
        'f_index.02.L': 'index_02_l',
        'f_index.03.R': 'index_03_r',
        'f_index.03.L': 'index_03_l',
        'f_middle.01.R': 'middle_01_r',
        'f_middle.01.L': 'middle_01_l',
        'f_middle.02.R': 'middle_02_r',
        'f_middle.02.L': 'middle_02_l',
        'f_middle.03.R': 'middle_03_r',
        'f_middle.03.L': 'middle_03_l',
        'f_ring.01.R': 'ring_01_r',
        'f_ring.01.L': 'ring_01_l',
        'f_ring.02.R': 'ring_02_r',
        'f_ring.02.L': 'ring_02_l',
        'f_ring.03.R': 'ring_03_r',
        'f_ring.03.L': 'ring_03_l',
        'f_pinky.01.R': 'pinky_01_r',
        'f_pinky.01.L': 'pinky_01_l',
        'f_pinky.02.R': 'pinky_02_r',
        'f_pinky.02.L': 'pinky_02_l',
        'f_pinky.03.R': 'pinky_03_r',
        'f_pinky.03.L': 'pinky_03_l',
        'thigh.R': 'thigh_r',
        'thigh.L': 'thigh_l',
        'shin.R': 'calf_r',
        'shin.L': 'calf_l',
        'foot.R': 'foot_r',
        'foot.L': 'foot_l',
        'heel.02.R': 'heel_r',
        'heel.02.L': 'heel_l',
    },
    "daz_g8.1": {
        'pelvis': 'hip',
        'spine': 'abdomenLower',
        'spine.001': 'chestLower',
        'neck': 'neckUpper',
        'face': 'head',
        'shoulder.R': 'rCollar',
        'shoulder.L': 'lCollar',
        'upper_arm.R': 'rShldrBend',
        'upper_arm.L': 'lShldrBend',
        'forearm.R': 'rForearmBend',
        'forearm.L': 'lForearmBend',
        'forearm_twist.R': 'rForearmTwist',
        'forearm_twist.L': 'lForearmTwist',
        'hand.R': 'rHand',
        'hand.L': 'lHand',
        'palm.01.R': 'rCarpal1',
        'palm.02.R': 'rCarpal2',
        'palm.03.R': 'rCarpal3',
        'palm.04.R': 'rCarpal4',
        'palm.01.L': 'lCarpal1',
        'palm.02.L': 'lCarpal2',
        'palm.03.L': 'lCarpal3',
        'palm.04.L': 'lCarpal4',
        'thumb.01.R': 'rThumb1',
        'thumb.01.L': 'lThumb1',
        'thumb.02.R': 'rThumb2',
        'thumb.02.L': 'lThumb2',
        'thumb.03.R': 'rThumb3',
        'thumb.03.L': 'lThumb3',
        'f_index.01.R': 'rIndex1',
        'f_index.01.L': 'lIndex1',
        'f_index.02.R': 'rIndex2',
        'f_index.02.L': 'lIndex2',
        'f_index.03.R': 'rIndex3',
        'f_index.03.L': 'lIndex3',
        'f_middle.01.R': 'rMid1',
        'f_middle.01.L': 'lMid1',
        'f_middle.02.R': 'rMid2',
        'f_middle.02.L': 'lMid2',
        'f_middle.03.R': 'rMid3',
        'f_middle.03.L': 'lMid3',
        'f_ring.01.R': 'rRing1',
        'f_ring.01.L': 'lRing1',
        'f_ring.02.R': 'rRing2',
        'f_ring.02.L': 'lRing2',
        'f_ring.03.R': 'rRing3',
        'f_ring.03.L': 'lRing3',
        'f_pinky.01.R': 'rPinky1',
        'f_pinky.01.L': 'lPinky1',
        'f_pinky.02.R': 'rPinky2',
        'f_pinky.02.L': 'lPinky2',
        'f_pinky.03.R': 'rPinky3',
        'f_pinky.03.L': 'lPinky3',
        'thigh.R': 'rThighBend',
        'thigh.L': 'lThighBend',
        'shin.R': 'rShin',
        'shin.L': 'lShin',
        'foot.R': 'rFoot',
        'foot.L': 'lFoot',
    }
}


def _build_mgear_mapping() -> dict:
    """Rigify -> mGear biped joint names.

    Two reasons this matters beyond convenience:

    * Rigify names contain dots (`f_index.01.L`). Dots are not legal in node names in
      several DCC packages, which escape them on FBX import - `f_index.01.L` arrives as
      `f_indexFBXASC04601FBXASC046L` - and that defeats any name-based retargeting. EVERY
      bone is renamed here, even ones with no mGear counterpart, so no dot survives the
      export.

    * mGear's finger components are indexed 0-3 rather than named, so index/middle/ring/pinky
      map onto finger_L0 .. finger_L3.

    Derived from a joint dump of a real mGear biped rig, not from documentation.
    """
    mapping = {
        'pelvis': 'spine_C0_pelvis_Jnt',
        'spine': 'spine_C0_spine_01_Jnt',
        'spine.001': 'spine_C0_spine_05_Jnt',   # chest: shoulders and neck attach here
        'neck': 'neck_C0_neck_01_Jnt',
        'face': 'neck_C0_head_Jnt',
    }
    # (rigify side suffix, mGear side token)
    for rig_side, mg in (('L', 'L0'), ('R', 'R0')):
        mapping.update({
            f'shoulder.{rig_side}': f'shoulder_{mg}_shoulder_Jnt',
            f'upper_arm.{rig_side}': f'arm_{mg}_upperarm_Jnt',
            f'forearm.{rig_side}': f'arm_{mg}_lowerarm_Jnt',
            f'hand.{rig_side}': f'arm_{mg}_hand_Jnt',
            f'thigh.{rig_side}': f'leg_{mg}_thigh_Jnt',
            f'shin.{rig_side}': f'leg_{mg}_calf_Jnt',
            f'foot.{rig_side}': f'leg_{mg}_foot_Jnt',
        })
        # mGear's thumb starts at the proximal phalanx; Rigify has an extra carpal.
        for i in (1, 2, 3):
            mapping[f'thumb.0{i}.{rig_side}'] = f'thumb_{mg}_thumb_0{i}_Jnt'
        # Metacarpals and fingers: index/middle/ring/pinky -> finger_?0 .. finger_?3
        for idx, rigify_finger in enumerate(('f_index', 'f_middle', 'f_ring', 'f_pinky')):
            mapping[f'palm.0{idx + 1}.{rig_side}'] = f'meta_{mg}_{idx}_Jnt'
            for joint in (1, 2, 3):
                mapping[f'{rigify_finger}.0{joint}.{rig_side}'] = \
                    f'finger_{rig_side}{idx}_finger_0{joint}_Jnt'

        # No mGear counterpart, but must still lose their dots so no importer mangles them.
        low = rig_side.lower()
        mapping[f'pelvis.{rig_side}'] = f'pelvis_{low}'       # mGear goes pelvis -> thigh
        mapping[f'thumb.carpal.{rig_side}'] = f'thumb_carpal_{low}'
        mapping[f'heel.02.{rig_side}'] = f'heel_{low}'        # mGear's ball_Jnt is a toe, not a heel
    return mapping


bone_naming_mapping["mgear"] = _build_mgear_mapping()