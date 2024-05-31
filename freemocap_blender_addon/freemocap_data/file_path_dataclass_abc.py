from pathlib import Path
from typing import Dict, Any, Union, Optional
from dataclasses import dataclass, field
from abc import ABC

@dataclass
class FilePathDataClass(ABC):
    def __init__(self, **kwargs: Union[str, Path, Any]):
        self.init_kwargs = kwargs
        # Convert all input paths to Path objects or nested FilePathDataClass instances
        converted_data = self._convert_str_to_path(self.init_kwargs)
        # Assign the converted data to the instance's __dict__
        for key, value in converted_data.items():
            setattr(self, key, value)
        self._validate_paths(self.__dict__)

    def __post_init__(self):
        # This method is called after the dataclass-generated __init__ method
        # We don't need to do anything here since the conversion and validation are done in our __init__
        pass

    def _convert_str_to_path(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively converts string values in a dictionary to Path objects
        """
        converted_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                converted_data[key] = self._convert_str_to_path(value)
            elif isinstance(value, FilePathDataClass):
                converted_data[key] = value
            else:
                converted_data[key] = Path(value) if isinstance(value, str) else value
        return converted_data

    def _validate_paths(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, Path):
                if not value.exists():
                    raise FileNotFoundError(f'File not found: {value}')
            elif isinstance(value, FilePathDataClass):
                self._validate_paths(value.__dict__)
            else:
                raise ValueError(f'Invalid type for {key}: {type(value)}. Expected `Path` or `FilePathDataClass`.')

    def __str__(self, level=0) -> str:
        indent = '\t' * level
        attributes = []
        for key, value in self.__dict__.items():
            if isinstance(value, FilePathDataClass):
                attributes.append(f'{indent}\t{key}: {value.__str__(level + 1)}')
            else:
                attributes.append(f'{indent}\t{key}: {value}')
        return f'{indent}{self.__class__.__name__}:\n' + "\n".join(attributes)


@dataclass
class ChildFilePathDataClass(FilePathDataClass):
    file2: str

@dataclass
class ParentFilePathDataClass(FilePathDataClass):
    file1: str
    child: ChildFilePathDataClass



if __name__ == "__main__":
    parent = ParentFilePathDataClass(file1='path/to/file1', child=ChildFilePathDataClass(file2='path/to/file2'))
    print(parent)
