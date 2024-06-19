from dataclasses import dataclass
from typing import get_type_hints, Any

import numpy as np


class TypeHintError(TypeError):
    """Custom error for type hint mismatches."""

    def __init__(self, field, expected_type, actual_value):
        self.field = field
        self.expected_type = expected_type
        self.actual_value = actual_value
        super().__init__(self._error_message())

    def _error_message(self):
        return (
            f"Expected type '{self.expected_type}' for field '{self.field}', "
            f"but got '{type(self.actual_value)}' with value '{self.actual_value}'"
        )




def is_compatible_type(value: Any, expected_type: Any) -> bool:
    """
    Check if the value is compatible with the expected type.
    """
    numpy_float_types = (np.float16, np.float32, np.float64)
    numpy_int_types = (np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)
    try:
        if isinstance(value, expected_type):
            return True
        if expected_type is float and isinstance(value, numpy_float_types):
            return True
        if expected_type is int and isinstance(value, numpy_int_types):
            return True
        if hasattr(expected_type, '__origin') and expected_type.__origin in (list, dict):
            return isinstance(value, expected_type.__origin)
    except Exception as e:
        print(f"Error checking type: {e.__class__.__name__} - {e} - while checking {value} against {expected_type}")

    return False



def enforce_type_hints(instance):
    def _enforce(instance, hints):
        for field, field_type in hints.items():
            value = getattr(instance, field)
            if hasattr(field_type, '__origin__') and field_type.__origin__ in (list, dict):
                # Handle generic types (e.g., List[int], Dict[str, int])
                origin_type = field_type.__origin__
                if not isinstance(value, origin_type):
                    raise TypeHintError(field, field_type, value)
                args = field_type.__args__
                if origin_type is list:
                    for item in value:
                        if not is_compatible_type(item, args[0]):
                            raise TypeHintError(field, field_type, value)
                elif origin_type is dict:
                    for key, val in value.items():
                        if not is_compatible_type(key, args[0]) or not is_compatible_type(val, args[1]):
                            raise TypeHintError(field, field_type, value)
            elif not is_compatible_type(value, field_type):
                if hasattr(field_type, '__dataclass_fields__'):
                    _enforce(value, get_type_hints(field_type))
                else:
                    raise TypeHintError(field, field_type, value)

    hints = get_type_hints(instance.__class__)
    _enforce(instance, hints)


@dataclass
class TypeSafeDataclass:
    def __post_init__(self):
        enforce_type_hints(self)
