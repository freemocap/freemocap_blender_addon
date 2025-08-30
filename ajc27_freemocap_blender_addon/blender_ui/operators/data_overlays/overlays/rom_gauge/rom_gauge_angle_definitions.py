# Definitions for various range of motion (ROM) angles
# It has definitions for non-calculated angles as well

# TODO: Adjust the vectors and rotation directions as needed based on testing
# TODO: Maybe add a view/side variable to complement the plane of rotation?.
# Like Left View/Side and Sagittal Plane, Front View/Side and Frontal Plane, Top View/Side and Transverse Plane
rom_gauge_angle_definitions = {
    'left_elbow_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': -1, # 1 is CCW, -1 is CW
    },
    'left_shoulder_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': None,  # No proximal segment for shoulder as the clavicle is normal to the rotation plane
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': -1,
    },
    'left_shoulder_abduction_adduction': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (-1, 0),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': 1,
    },
    'left_shoulder_rotation': { # non-calculated angle
        'reference_vector': (1, 0),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Transverse Plane',
        'rotation_direction': 1,
    },
    'right_elbow_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'right_shoulder_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': None,  # No proximal segment for shoulder as the clavicle is normal to the rotation plane
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'right_shoulder_abduction_adduction': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (1, 0),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': -1,
    },
    'right_shoulder_rotation': { # non-calculated angle
        'reference_vector': (1, 0),
        'proximal_segment_vector': (1, 0),
        'rotation_plane_name': 'Transverse Plane',
        'rotation_direction': 1,
    },
    'left_knee_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'left_hip_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': None,  # No proximal segment for hip as the pelvis is normal to the rotation plane
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': -1,
    },
    'left_hip_abduction_adduction': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (-1, 0),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': 1,
    },
    'left_hip_rotation': { # non-calculated angle
        'reference_vector': (1, 0),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Transverse Plane',
        'rotation_direction': 1,
    },
    'right_knee_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': -1,
    },
    'right_hip_extension_flexion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': None,  # No proximal segment for hip as the pelvis is normal to the rotation plane
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'right_hip_abduction_adduction': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (1, 0),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': -1,
    },
    'right_hip_rotation': { # non-calculated angle
        'reference_vector': (1, 0),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Transverse Plane',
        'rotation_direction': 1,
    },
    'neck_extension_flexion': {
        'reference_vector': (0, 1),
        'proximal_segment_vector': (0, -1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'neck_lateral_flexion': {
        'reference_vector': (0, 1),
        'proximal_segment_vector': (0, -1),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': -1,
    },
    'neck_rotation': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': None,  # No proximal segment for neck as the torso is normal to the rotation plane
        'rotation_plane_name': 'Transverse Plane',
        'rotation_direction': -1,
    },
    'left_ankle_dorsiflexion_plantarflexion': {
        'reference_vector': (-1, 0),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': -1,
    },
    'left_ankle_inversion_eversion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': -1,
    },
    'right_ankle_dorsiflexion_plantarflexion': {
        'reference_vector': (1, 0),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'right_ankle_inversion_eversion': {
        'reference_vector': (0, -1),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': 1,
    },
    'spine_extension_flexion': {
        'reference_vector': (0, 1),
        'proximal_segment_vector': (0, -1),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'spine_lateral_flexion': {
        'reference_vector': (0, 1),
        'proximal_segment_vector': (0, -1),
        'rotation_plane_name': 'Frontal Plane',
        'rotation_direction': 1,
    },
    'spine_rotation': {
        'reference_vector': (1, 0),
        'proximal_segment_vector': (0, 1),
        'rotation_plane_name': 'Transverse Plane',
        'rotation_direction': 1,
    },
    'left_hand_extension_flexion': {
        'reference_vector': (-1, 0),
        'proximal_segment_vector': (1, 0),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': 1,
    },
    'right_hand_extension_flexion': {
        'reference_vector': (1, 0),
        'proximal_segment_vector': (-1, 0),
        'rotation_plane_name': 'Sagittal Plane',
        'rotation_direction': -1,
    },
}