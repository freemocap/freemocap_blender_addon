import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class FootLockingProperties(bpy.types.PropertyGroup):
    show_foot_locking_options: PropertyTypes.Bool(
        description = 'Toggle Foot Locking Options'
    ) # type: ignore
    foot_locking_method: PropertyTypes.Enum(
        description = 'Foot locking method',
        items = [('foot_group_movement', 'Foot Group Movement', ''),
                 ('individual_marker_height', 'Individual Marker Height', ''),
                 ('window_3d_compensation', 'Window 3D Compensation', '')
        ]
    ) # type: ignore

    # ── Individual Marker Height (imh) Properties ────────────────────

    show_imh_options: PropertyTypes.Bool(
        description = 'Toggle Individual Marker Height Options'
    ) # type: ignore
    imh_target_foot: PropertyTypes.Enum(
        description = 'Target foot for applying foot locking',
        items = [('both_feet', 'Both Feet', ''),
                 ('left_foot', 'Left Foot', ''),
                 ('right_foot', 'Right Foot', '')
                ]
    ) # type: ignore
    imh_target_base_markers: PropertyTypes.Enum(
        description = 'Target foot base markers for applying foot locking',
        items = [('foot_index_and_heel', 'foot_index and heel', ''),
                 ('foot_index', 'foot_index', ''),
                 ('heel', 'heel', '')
                ]
    ) # type: ignore
    imh_z_threshold: PropertyTypes.Float(
        default = 0.02,
        precision = 3,
        description = 'Vertical threshold under which foot markers are '
                      'considered for applying foot locking'
    ) # type: ignore
    imh_ground_level: PropertyTypes.Float(
        precision = 3,
        description = 'Ground level for foot locking. Markers with z global '
                      'coordinate lower than this value will be fixed to '
                      'this level. It must be lower than the z threshold'
    ) # type: ignore
    imh_frame_window_min_size: PropertyTypes.Int(
        default = 10,
        min = 1,
        description = 'Minimum number of consecutive frames a marker must '
                      'be below the z threshold to trigger foot locking'
    ) # type: ignore
    imh_initial_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'Number of frames at the start of a locked window '
                      'where the z correction is attenuated by a quadratic '
                      'ease-in function'
    ) # type: ignore
    imh_final_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'Number of frames at the end of a locked window '
                      'where the z correction is attenuated by a quadratic '
                      'ease-out function'
    ) # type: ignore
    imh_lock_xy_at_ground_level: PropertyTypes.Bool(
        description = 'When applying foot locking, also lock the X and Y '
                      'coordinates at ground level. Useful when standing '
                      'still but may cause sticky feet during walking'
    ) # type: ignore
    imh_knee_hip_compensation_coefficient: PropertyTypes.FloatVector(
        size = 3,
        subtype = 'NONE',
        min = 0.0,
        max = 1.0,
        default = (0.0, 0.0, 1.0),
        description = 'Per-axis (X, Y, Z) multiplier for knee and hip '
                      'adjustment when the ankle position changes. '
                      'Default (0, 0, 1) applies only vertical compensation'
    ) # type: ignore
    imh_compensate_upper_body: PropertyTypes.Bool(
        default = True,
        description = 'Propagate the foot locking z delta to the upper body '
                      'markers via the hips_center and trunk_center chain'
    ) # type: ignore

    # ── Window 3D Compensation (w3d) Properties ──────────────────────

    show_w3d_options: PropertyTypes.Bool(
        description = 'Toggle Window 3D Compensation Options'
    ) # type: ignore
    w3d_target_foot: PropertyTypes.Enum(
        description = 'Target foot for applying foot locking',
        items = [('both_feet', 'Both Feet', ''),
                 ('left_foot', 'Left Foot', ''),
                 ('right_foot', 'Right Foot', '')
                ]
    ) # type: ignore
    w3d_target_base_markers: PropertyTypes.Enum(
        description = 'Target foot base markers for applying foot locking',
        items = [('foot_index_and_heel', 'foot_index and heel', ''),
                 ('foot_index', 'foot_index', ''),
                 ('heel', 'heel', '')
                ]
    ) # type: ignore
    w3d_z_threshold: PropertyTypes.Float(
        default = 0.02,
        precision = 3,
        description = 'Vertical threshold under which foot markers are '
                      'considered for applying foot locking'
    ) # type: ignore
    w3d_ground_level: PropertyTypes.Float(
        precision = 3,
        description = 'Ground level for foot locking. Markers with z global '
                      'coordinate lower than this value will be fixed to '
                      'this level. It must be lower than the z threshold'
    ) # type: ignore
    w3d_frame_window_min_size: PropertyTypes.Int(
        default = 10,
        min = 1,
        description = 'Minimum number of consecutive frames a marker must '
                      'be below the z threshold to trigger foot locking'
    ) # type: ignore
    w3d_initial_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'Number of frames at the start of a locked window '
                      'where the correction is attenuated by a quadratic '
                      'ease-in function'
    ) # type: ignore
    w3d_final_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'Number of frames at the end of a locked window '
                      'where the correction is attenuated by a quadratic '
                      'ease-out function'
    ) # type: ignore
    w3d_lock_xy_at_ground_level: PropertyTypes.Bool(
        description = 'When applying foot locking, also lock the X and Y '
                      'coordinates at ground level. Useful when standing '
                      'still but may cause sticky feet during walking'
    ) # type: ignore
    w3d_knee_hip_compensation_coefficient: PropertyTypes.FloatVector(
        size = 3,
        subtype = 'NONE',
        min = 0.0,
        max = 1.0,
        default = (0.0, 0.0, 1.0),
        description = 'Per-axis (X, Y, Z) multiplier for knee and hip '
                      'adjustment when the ankle position changes. '
                      'Default (0, 0, 1) applies only vertical compensation'
    ) # type: ignore
    w3d_compensate_upper_body: PropertyTypes.Bool(
        default = True,
        description = 'Propagate the foot locking z delta to the upper body '
                      'markers via the hips_center and trunk_center chain'
    ) # type: ignore

    # ── Foot Group Movement (fgm) Properties ─────────────────────────

    show_fgm_options: PropertyTypes.Bool(
        description = 'Toggle Foot Group Movement Options'
    ) # type: ignore
    fgm_target_foot: PropertyTypes.Enum(
        description = 'Target foot for applying foot locking',
        items = [('both_feet', 'Both Feet', ''),
                 ('left_foot', 'Left Foot', ''),
                 ('right_foot', 'Right Foot', '')
                ]
    ) # type: ignore
    fgm_z_threshold: PropertyTypes.Float(
        default = 0.02,
        precision = 3,
        description = 'Vertical threshold under which foot markers are '
                      'considered for applying foot locking'
    ) # type: ignore
    fgm_ground_level: PropertyTypes.Float(
        precision = 3,
        description = 'Ground level for foot locking. Markers with z global '
                      'coordinate lower than this value will be fixed to '
                      'this level. It must be lower than the z threshold'
    ) # type: ignore
    fgm_frame_window_min_size: PropertyTypes.Int(
        default = 10,
        min = 1,
        description = 'Minimum number of consecutive frames a marker must '
                      'be below the z threshold to trigger foot locking'
    ) # type: ignore
    fgm_initial_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'Number of frames at the start of a locked block '
                      'where the correction is attenuated by a quadratic '
                      'ease-in function'
    ) # type: ignore
    fgm_knee_hip_compensation_coefficient: PropertyTypes.FloatVector(
        size = 3,
        subtype = 'NONE',
        min = 0.0,
        max = 1.0,
        default = (0.0, 0.0, 1.0),
        description = 'Per-axis (X, Y, Z) multiplier for knee and hip '
                      'adjustment when the ankle position changes. '
                      'Default (0, 0, 1) applies only vertical compensation'
    ) # type: ignore
    fgm_compensate_upper_body: PropertyTypes.Bool(
        default = True,
        description = 'Propagate the foot locking z delta to the upper body '
                      'markers via the hips_center and trunk_center chain'
    ) # type: ignore
    fgm_negative_height_limit: PropertyTypes.Float(
        default = 0.02,
        precision = 3,
        description = 'Maximum vertical lift applied to the leg when a foot '
                      'marker dips below ground. Limits how much the body '
                      'is raised. Excess depth is compensated by foot rotation'
    ) # type: ignore
    fgm_xy_radius: PropertyTypes.Float(
        default = 0.05,
        precision = 3,
        description = 'Maximum XY distance from the moving average position '
                      'for a frame to be considered a lock candidate. '
                      'Filters out frames where the foot is moving laterally'
    ) # type: ignore
    fgm_moving_average_window: PropertyTypes.Int(
        default = 5,
        min = 1,
        description = 'Number of frames before and after the current frame '
                      'used to calculate the XY moving average position'
    ) # type: ignore
