import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes
from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles

def get_joint_angle_items():
    joint_angle_items = []

    joint_angle_items.append(('all', 'All', ''))

    # Get the segments of all the joint angles
    joint_angle_segments = list(set([joint_angle['segment'] for joint_angle in joint_angles.values()]))

    for segment in joint_angle_segments:
        segment_title = 'Segment: ' + segment.replace('_', ' ').title()
        joint_angle_items.append(('segment#' + segment, segment_title, ''))

    for key in joint_angles.keys():
        key_title = key.replace('_', ' ').title()
        joint_angle_items.append((key, key_title, ''))
        
    return joint_angle_items

class AddJointAnglesProperties(bpy.types.PropertyGroup):
    show_add_joint_angles_options: PropertyTypes.Bool(
        description = 'Toggle Add Joint Angles Options'
    ) # type: ignore

    joint_angle: PropertyTypes.Enum(
        description = 'Joint Angle',
        items = get_joint_angle_items()
    ) # type: ignore

    joint_angle_radius: PropertyTypes.Float(
        default = 10,
        min = 0.0,
        description = 'Joint Angle Radius (in centimeters)'
    ) # type: ignore

    joint_angle_overwrite_colors: PropertyTypes.Bool(
        default = False,
        description = 'Overwrite Default Joint Angle Colors'
    ) # type: ignore

    joint_angle_color: PropertyTypes.FloatVector(
        default = tuple((0.694,0.082,0.095,1.0))
    ) # type: ignore

    joint_angle_text_color: PropertyTypes.FloatVector(
        default = tuple((1.0,0.365,0.048,1.0))
    ) # type: ignore

    joint_angle_text_size: PropertyTypes.Float(
        default = 5.0,
        min = 0.0,
        description = 'Joint Angle Text Size [cm]'
    ) # type: ignore

    joint_angle_text_orientation: PropertyTypes.Enum(
        description = 'Joint Angle Text Orientation',
        items = [
            ('rotation_plane_normal', 'Rotation Plane Normal', ''),
            ('global_x', 'Global X', ''),
            ('global_y', 'Global Y', ''),
            ('global_z', 'Global Z', ''),
            ('global_-x', 'Global -X', ''),
            ('global_-y', 'Global -Y', ''),
            ('global_-z', 'Global -Z', ''),
        ]
    ) # type: ignore

    joint_angle_text_local_x_offset: PropertyTypes.Float(
        default = 3.0,
        description = 'Joint Angle Text Local X Offset [cm]'
    ) # type: ignore

    joint_angle_text_local_y_offset: PropertyTypes.Float(
        default = 0.0,
        description = 'Joint Angle Text Local Y Offset [cm]'
    ) # type: ignore
