import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class LimitMarkersRangeOfMotionProperties(bpy.types.PropertyGroup):
    show_limit_markers_range_of_motion_options: PropertyTypes.Bool(
        description = 'Toggle Limit Markers Range of Motion Options'
    ) # type: ignore

    limit_palm_markers: PropertyTypes.Bool(
        name='',
        description='Limit the range of motion of the palm markers',
        default=False,
    )  # type: ignore

    limit_proximal_phalanx_markers: PropertyTypes.Bool(
        name='',
        description='Limit the range of motion of the proximal phalanx markers',
        default=True,
    )  # type: ignore

    limit_intermediate_phalanx_markers: PropertyTypes.Bool(
        name='',
        description='Limit the range of motion of the intermediate phalanx markers',
        default=True,
    )  # type: ignore

    limit_distal_phalanx_markers: PropertyTypes.Bool(
        name='',
        description='Limit the range of motion of the distal phalanx markers',
        default=True,
    )  # type: ignore

    range_of_motion_scale: PropertyTypes.Float(
        name='',
        description=(
            'Scale the range of motion of the markers (rotation_limit_max - rotation_limit_min).'
            + ' A value of 1.0 keeps the range equal to the one defined in BONE_DEFINITIONS.'
            + ' A value of 0.5 halves the range (thightens the ROM).'
            + ' A value of 2.0 doubles the range (loosens the ROM).'
            + ' A value of 0.0 fixes the markers to a cupped hand pose (needs research why this happens).'
            + 'Use a high value (like 500) to set the ranges to a max of [-180º, 180º].'
        ),
        default=1.0,
        precision=2,
    )  # type: ignore

    hand_locked_track_marker: PropertyTypes.Enum(
        name='',
        description=(
            'Hand locked track marker where the z axis points to.'
            + ' Useful when calculating the initial hand axes.'
        ),
        items = [
            ('hand_index_finger_mcp', 'hand_index_finger_mcp', ''),
            ('index', 'index', ''),
            ('hand_thumb_cmc', 'hand_thumb_cmc', ''),            
        ]
    )  # type: ignore

    hand_damped_track_marker: PropertyTypes.Enum(
        name='',
        description=(
            'Hand damped track marker where the y axis points to.'
            + ' Useful when calculating the initial hand axes.'
        ),
        items = [
            ('hand_middle_finger_mcp', 'hand_middle_finger_mcp', ''),
            ('hand_middle', 'hand_middle', ''),            
        ]
    )  # type: ignore


