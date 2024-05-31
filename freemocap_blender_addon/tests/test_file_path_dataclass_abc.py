from dataclasses import dataclass
from typing import Dict

from freemocap_blender_addon.freemocap_data.file_path_dataclass_abc import FilePathDataClass
from pathlib import Path

@dataclass
class ChildFilePathDataClass(FilePathDataClass):
    file1: Path
    file2: Path

# Valid parent class
@dataclass
class ParentFilePathDataClass(FilePathDataClass):
    file1: Path
    child: ChildFilePathDataClass

# Invalid child class (contains non-existent paths)
@dataclass
class InvalidChildFilePathDataClass(FilePathDataClass):
    file1: Path
    file2: Path

# Invalid parent class (contains non-existent paths)
@dataclass
class InvalidParentFilePathDataClass(FilePathDataClass):
    file1: Path
    child: InvalidChildFilePathDataClass

def safe_validate_paths(data: Dict[str, Any]):
    try:
        for key, value in data.items():
            if isinstance(value, Path):
                if not value.exists():
                    raise FileNotFoundError(f'File not found: {value}')
            elif isinstance(value, FilePathDataClass):
                safe_validate_paths(value.__dict__)
            else:
                raise ValueError(f'Invalid type for {key}: {type(value)}. Expected `Path` or `FilePathDataClass`.')
    except Exception as e:
        return str(e)
    return None

def test_FilePathDataClass_initialization_and_conversion():
    """Test the initialization and path conversion of FilePathDataClass."""
    test_class = FilePathDataClass(file1="path/to/file1", file2="path/to/file2")
    assert isinstance(test_class.file1, Path)
    assert isinstance(test_class.file2, Path)
    assert str(test_class.file1) == "path/to/file1"
    assert str(test_class.file2) == "path/to/file2"

def test_FilePathDataClass_nested_initialization():
    """Test the nested initialization of FilePathDataClass."""
    nested = FilePathDataClass(file1="path/to/file1")
    test_class = FilePathDataClass(file1="path/to/file1", nested=nested)
    assert isinstance(test_class.file1, Path)
    assert isinstance(test_class.nested, FilePathDataClass)
    assert isinstance(test_class.nested.file1, Path)
    assert str(test_class.nested.file1) == "path/to/file1"

def test_FilePathDataClass_validation():
    """Test the validation process for FilePathDataClass."""
    # Assuming "path/to/file1" and "path/to/file2" are non-existent paths
    error_message = safe_validate_paths({"file1": Path("path/to/file1"), "file2": Path("path/to/file2")})
    assert error_message == 'File not found: path/to/file1'

def test_FilePathDataClass_invalid_type():
    """Test invalid type handling in FilePathDataClass."""
    error_message = safe_validate_paths({"file1": 123})
    assert error_message == 'Invalid type for file1: <class \'int\'>. Expected `Path` or `FilePathDataClass`.'
