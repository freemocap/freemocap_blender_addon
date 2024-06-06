from enum import Enum

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointMapping


def build_enum_from_dict(enum_name: str,
                         enum_dict: dict):
    enum_members = {
        key: KeypointMapping(mapping=value)
        for key, value in enum_dict.items()
    }
    return Enum(enum_name, enum_members)
