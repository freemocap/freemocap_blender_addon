"""Optional Blender-only edits; never save source recording trajectories."""
import json
import bpy


def apply_cleanup(root, *, foot_locking=False, hand_limits=False):
    if not foot_locking and not hand_limits:
        return
    from ..utilities.animation_targets import animation_targets
    scene = bpy.context.scene
    animation_targets(root, scene.frame_start, scene.frame_end)  # validate before editing
    frame = scene.frame_current
    try:
        if foot_locking:
            from ..blender_ui.operators.animation.foot_locking.methods.foot_group_movement import run_foot_group_movement
            run_foot_group_movement(root, scene.frame_start, scene.frame_end)
        if hand_limits:
            from ..blender_ui.operators.animation.limit_markers_range_of_motion.limit_markers_range_of_motion import limit_markers_range_of_motion
            limit_markers_range_of_motion(root, scene.frame_start, scene.frame_end)
        root['animation_cleanup'] = json.dumps(dict(foot_locking=foot_locking, hand_limits=hand_limits,
            scope='Blender constraint targets only; recorded landmarks, segment poses and COM remain unchanged'))
    finally:
        scene.frame_set(frame)
