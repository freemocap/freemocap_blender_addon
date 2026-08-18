# Function to translate a marker's fcurve frame position by a delta
def translate_marker(
    hierarchy,
    markers,
    marker_name,
    delta,
    frame,
):
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
