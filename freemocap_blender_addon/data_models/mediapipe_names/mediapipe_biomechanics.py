joints_angle_points = {
    'right_shoulder': {'parent': 'neck_center', 'child': 'right_elbow'},
    'left_shoulder': {'parent': 'neck_center', 'child': 'left_elbow'},
    'right_elbow': {'parent': 'right_shoulder', 'child': 'right_wrist'},
    'left_elbow': {'parent': 'left_shoulder', 'child': 'left_wrist'},
    'right_wrist': {'parent': 'right_elbow', 'child': 'right_hand_middle'},
    'left_wrist': {'parent': 'left_elbow', 'child': 'left_hand_middle'},
    'right_hip': {'parent': 'hips_center', 'child': 'right_knee'},
    'left_hip': {'parent': 'hips_center', 'child': 'left_knee'},
    'right_knee': {'parent': 'right_hip', 'child': 'right_ankle'},
    'left_knee': {'parent': 'left_hip', 'child': 'left_ankle'},
    'right_ankle': {'parent': 'right_knee', 'child': 'right_foot_index'},
    'left_ankle': {'parent': 'left_knee', 'child': 'left_foot_index'},
}
ground_contact_points = [
    'right_heel',
    'left_heel',
    'right_foot_index',
    'left_foot_index',
]
