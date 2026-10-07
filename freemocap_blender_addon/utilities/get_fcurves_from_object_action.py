"""Read either legacy actions or the object's own slot in layered actions."""
def get_fcurves_from_object_action(obj):
    if not obj or not obj.animation_data or not obj.animation_data.action:
        return None
    animation = obj.animation_data
    action = animation.action
    slot = getattr(animation, 'action_slot', None)
    if slot is not None:
        for layer in action.layers:
            for strip in layer.strips:
                if hasattr(strip, 'channelbag'):
                    bag = strip.channelbag(slot)
                    if bag is not None:
                        return bag.fcurves
        return None
    return getattr(action, 'fcurves', None)
