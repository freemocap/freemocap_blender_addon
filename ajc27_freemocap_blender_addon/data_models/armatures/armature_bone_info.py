from dataclasses import dataclass


@dataclass
class ArmatureBoneInfo:
    parent_bone: str
    connected: bool = True
    parent_position: str = "tail"
    default_length: float = 0