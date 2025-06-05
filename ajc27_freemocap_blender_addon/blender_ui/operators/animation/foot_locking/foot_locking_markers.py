"""
Dictionary containing markers for foot locking, including base, ankle,
bones, and compensation markers for left and right feet.
"""
foot_locking_markers = {
    'left_foot': {
        'base': ['left_foot_index', 'left_heel'],
        'ankle': ['left_ankle'],
        'bones': ['foot.L', 'heel.02.L'],
        'compensation_markers': ['left_knee', 'left_hip']
    },
    'right_foot': {
        'base': ['right_foot_index', 'right_heel'],
        'ankle': ['right_ankle'],
        'bones': ['foot.R', 'heel.02.R'],
        'compensation_markers': ['right_knee', 'right_hip']
    }
}
