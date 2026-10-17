"""Full rigid attachment frames; a direction alone does not resolve roll."""
from mathutils import Matrix, Vector


def basis(primary, roll_reference):
    primary = Vector(primary)
    secondary = Vector(roll_reference)
    if primary.length < 1e-8:
        raise ValueError('Zero attachment direction')
    primary.normalize()
    secondary -= primary * secondary.dot(primary)
    if secondary.length < 1e-6:
        raise ValueError('Attachment roll reference is parallel to its primary direction')
    secondary.normalize()
    return Matrix((primary, secondary, primary.cross(secondary))).transposed()


def attachment_rotation(source_direction, local_direction, rest_rotation, roll_reference,
                        local_secondary=None):
    """Map canonical asset into owning segment local space.

    Prefer a declared anatomical secondary landmark in segment-local space.
    Otherwise the asset's rest-world roll reference specifies the binding roll
    for segments with only a primary landmark. This never reconstructs poses.
    """
    source = basis(source_direction, roll_reference)
    if local_secondary is not None:
        return basis(local_direction, local_secondary) @ source.transposed()
    target = basis(rest_rotation @ Vector(local_direction), roll_reference)
    return rest_rotation.to_matrix().transposed() @ target @ source.transposed()
