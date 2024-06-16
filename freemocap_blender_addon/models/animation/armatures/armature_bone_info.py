from dataclasses import dataclass

from freemocap_blender_addon.models.animation.armatures.rest_pose import BonePoseDefinition


@dataclass
class ArmatureBoneDefinition:
    rest_pose: BonePoseDefinition
    length: float
