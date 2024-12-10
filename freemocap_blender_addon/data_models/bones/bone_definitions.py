from pathlib import Path
from typing import Dict

from freemocap_blender_addon.data_models.bones.bone_definition_models import BoneDefinition

DEFAULT_BONE_DEFINITIONS_JSON_NAME = str(Path(__file__).parent / "default_bone_definitions.json")


def get_bone_definitions() -> Dict[str, BoneDefinition]:
    import json
    from freemocap_blender_addon.data_models.bones.bone_definition_models import BoneDefinition

    with open(DEFAULT_BONE_DEFINITIONS_JSON_NAME, 'r') as file:
        bone_definitions = json.load(file)

    return {name: BoneDefinition(**bone) for name, bone in bone_definitions.items()}
