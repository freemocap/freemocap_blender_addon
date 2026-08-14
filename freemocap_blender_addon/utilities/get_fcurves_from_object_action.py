import bpy

def get_fcurves_from_object_action(obj):
    """
    Helper to get fcurves from an object's action, 
    compatible with Blender < 5.0 and Blender 5.0+ (Slotted Actions).
    """
    if not obj or not obj.animation_data or not obj.animation_data.action:
        return None

    ad = obj.animation_data
    action = ad.action

    # In Blender < 5.0 (or for Legacy Actions in 5.0), Action has .fcurves
    if hasattr(action, "fcurves"):
        return action.fcurves

    # Blender 5.0+ Slotted Action logic
    try:
        from bpy_extras import anim_utils
        # Use the helper to get the channel bag for the current slot
        # ad.action_slot is available in 5.0 (and experimental in 4.3)
        slot = getattr(ad, "action_slot", None)
        if slot is not None:
            channelbag = anim_utils.action_get_channelbag_for_slot(action, slot)
            if channelbag:
                return channelbag.fcurves
    except (ImportError, AttributeError):
        pass

    return None
