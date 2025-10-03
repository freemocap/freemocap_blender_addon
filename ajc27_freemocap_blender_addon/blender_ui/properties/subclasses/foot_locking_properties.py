import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class FootLockingProperties(bpy.types.PropertyGroup):
    show_foot_locking_options: PropertyTypes.Bool(
        description = 'Toggle Foot Locking Options'
    ) # type: ignore
    foot_locking_method: PropertyTypes.Enum(
        description = 'Foot locking method',
        items = [('individual_marker_height', 'Individual Marker Height', ''),
        ]
    ) # type: ignore
    show_individual_marker_height_options: PropertyTypes.Bool(
        description = 'Toggle Individual Marker Height Options'
    ) # type: ignore
    target_foot: PropertyTypes.Enum(
        description = 'Target foot for applying foot locking',
        items = [('both_feet', 'Both Feet', ''),
                 ('left_foot', 'Left Foot', ''),
                 ('right_foot', 'Right Foot', '')
                ]
    ) # type: ignore
    target_base_markers: PropertyTypes.Enum(
        description = 'Target foot base markers for applying foot locking',
        items = [('foot_index_and_heel', 'foot_index and heel', ''),
                 ('foot_index', 'foot_index', ''),
                 ('heel', 'heel', '')
                ]
    ) # type: ignore
    z_threshold: PropertyTypes.Float(
        default = 0.02,
        precision = 3,
        description = 'Vertical threshold under which foot markers are '
                      'considered for applying foot locking'
    ) # type: ignore
    ground_level: PropertyTypes.Float(
        precision = 3,
        description = 'Ground level for applying foot locking. Markers with '
                      'z global coordinate lower than this value will be '
                      'fixed to this level. It must be lower than the '
                      'z threshold'
    ) # type: ignore
    frame_window_min_size: PropertyTypes.Int(
        default = 10,
        min = 1,
        description = 'Minimum frame window size for applying foot locking. '
                      'A markers z global coordinate has to be lower than the '
                      'z threshold for a consecutive frames count equal or '
                      'bigger than this value.'
                      'It must be equal or greater than '
                      'initial_attenuation_count + final_attenuation_count'
    ) # type: ignore
    initial_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'This are the first frames of the window which have '
                      'their z coordinate attenuated by the the initial '
                      'quadratic attenuation function'
    ) # type: ignore
    final_attenuation_count: PropertyTypes.Int(
        default = 5,
        min = 0,
        description = 'This are the last frames of the window which have '
                      'their z coordinate attenuated by the the final '
                      'quadratic attenuation function'
    ) # type: ignore
    lock_xy_at_ground_level: PropertyTypes.Bool(
        description = 'When applying foot locking, lock also the x and y '
                      'coordinates at the ground level. This is useful only '
                      'when character is standing still as it might leed to '
                      '"sticky" or "lead" feet effect'
    ) # type: ignore
    knee_hip_compensation_coefficient: PropertyTypes.Float(
        default = 1.0,
        precision = 3,
        min = 0.0,
        max = 1.0,
        description = 'After calculating the ankle new z global coordinate, '
                      'the knee and hip markers will be adjusted on the z '
                      'axis by the same delta multiplied by this coefficient.'
                      'A value of 1.0 means knee and hip have the same '
                      'adjustment as the ankle. A value of 0 means knee and '
                      'hip have no adjustment at all. Values lower than 1.0 '
                      'are useful when the rig has IK constraints on the legs.'
                      'This way the ankle adjustment is compensated by the '
                      'knee IK bending'
    ) # type: ignore
    compensate_upper_body: PropertyTypes.Bool(
        default = True,
        description = 'Compensate the upper body markers by setting the new '
                      'z coordinate of the hips_center marker as the average '
                      'z coordinate of left and right hips markers.'
                      'Then propagate the new z delta to the upper body '
                      'markers starting from the trunk_center.'
    ) # type: ignore
