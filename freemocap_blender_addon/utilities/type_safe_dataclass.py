from dataclasses import dataclass
from typing import get_type_hints, List, Dict, Any, Union

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
                        if not isinstance(item, args[0]):
                            raise TypeHintError(field, field_type, value)
                elif origin_type is dict:
                    for key, val in value.items():
                        if not isinstance(key, args[0]) or not isinstance(val, args[1]):
                            raise TypeHintError(field, field_type, value)
            elif not isinstance(value, field_type):
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
