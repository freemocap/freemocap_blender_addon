import json
from dataclasses import fields, is_dataclass
from typing import Optional

from .parameter_models import Config


def _section_from_dict(section_cls, data):
    """Build a Config sub-dataclass from a (possibly partial) dict.

    Unknown keys are ignored rather than raising, so a config payload produced by a
    newer freemocap than this addon still loads (the extra options are dropped).
    """
    if not is_dataclass(section_cls) or not isinstance(data, dict):
        return data

    known_field_names = {f.name for f in fields(section_cls)}
    unknown_field_names = set(data) - known_field_names
    if unknown_field_names:
        print(f"Ignoring unknown {section_cls.__name__} option(s): {sorted(unknown_field_names)}")

    return section_cls(**{name: data[name] for name in known_field_names if name in data})


def load_parameters_config_from_dict(data: Optional[dict]) -> Config:
    """Build a Config from a partial dict, falling back to defaults for omitted sections."""
    data = data or {}
    return Config(**{
        f.name: _section_from_dict(f.type, data.get(f.name, {}))
        for f in fields(Config)
    })


def load_default_parameters_config(filename: Optional[str] = None) -> Config:
    if filename is not None:
        with open(filename, "r") as f:
            return load_parameters_config_from_dict(json.load(f))
    else:
        return Config()


if __name__ == "__main__":
    from pprint import pprint as print

    default_parameters_filename = "default_parameters.json"
    config = load_default_parameters_config("default_parameters.json")
    print(config.__dict__)
