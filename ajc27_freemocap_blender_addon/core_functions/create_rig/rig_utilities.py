import re
from typing import Optional, List




def get_appended_number(rig_name: str) -> Optional[str]:
    pattern = r"\.0[0-9]{2}$"
    match = re.search(pattern, rig_name)
    return match.group() if match else None


def get_actual_empty_target_name(empty_names: List[str], base_target_name: str) -> str:
    """
    Get the actual empty target name based on the constraint target name,
    this is mostly to give us the ability to load multiple recorings, because
    blender will append `.001`, `.002`  the names of emtpies of the 2nd, 3rd, etc to avoid name collisions

    So basically, if the base_target name is `hips_center` this will look for empties named `hips_center`,
      `hips_center.001`, `hips_center.002`, etc in the provided `empty_names` list and return that
    """

    actual_target_name = None
    for empty_name in empty_names:
        if base_target_name in empty_name:
            actual_target_name = empty_name
            break

    if actual_target_name is None:
        raise ValueError(f"Could not find empty target for {base_target_name}")

    return actual_target_name
