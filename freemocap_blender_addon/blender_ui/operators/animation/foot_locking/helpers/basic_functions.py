# Function to translate a marker's fcurve frame position by a delta
def translate_marker(
    hierarchy,
    markers,
    marker_name,
    delta,
    frame,
):
    # Optional tracker aliases/hand points may be absent from a constraint rig.
    # Continue through the hierarchy so existing descendants still receive the edit.
    if marker_name in markers:
        markers[marker_name]['fcurves'][:, frame] += delta

    if marker_name in hierarchy and hierarchy[marker_name]['children']:
        for child in hierarchy[marker_name]['children']:
            translate_marker(
                hierarchy,
                markers,
                child,
                delta,
                frame,
            )

    return
