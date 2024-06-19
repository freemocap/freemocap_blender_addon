from dataclasses import dataclass
from pathlib import Path

from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class PathsDataclass(TypeSafeDataclass):
    def __post_init__(self):
        for field in self.__dict__.values():
            if isinstance(field, Path):
                if not field.exists():
                    raise FileNotFoundError(f"Path {field} does not exist")

    def __str__(self):
        classname = self.__class__.__name__
        fields = [f"\t{k}: {v}" for k, v in self.__dict__.items()]
        joined_fields = "\n".join(fields)
