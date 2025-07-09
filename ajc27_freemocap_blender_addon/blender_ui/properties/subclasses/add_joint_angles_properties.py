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
        joint_angle_items.append(('segment_' + segment, segment_title, ''))

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

    joint_angle_color: PropertyTypes.FloatVector(
        default = tuple((0.694,0.082,0.095,1.0))
    ) # type: ignore

    joint_angle_text_color: PropertyTypes.FloatVector(
        default = tuple((1.0,0.365,0.048,1.0))
    ) # type: ignore
