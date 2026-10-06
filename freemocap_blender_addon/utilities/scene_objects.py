"""Object traversal without the Blender 4.x children_recursive property."""


def descendants(obj):
    if obj is None:
        return []
    result = []
    pending = list(obj.children)
    while pending:
        child = pending.pop()
        result.append(child)
        pending.extend(child.children)
    return result
