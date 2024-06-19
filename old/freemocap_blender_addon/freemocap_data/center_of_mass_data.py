from dataclasses import dataclass
from typing import Self

import numpy as np
from freemocap_blender_addon.freemocap_data.data_component_abc import SkeletonDataComponent, ComponentType
from freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths import FreemocapDataPaths
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType


@dataclass
class CenterOfMassData:
    total_body_center_of_mass: SkeletonDataComponent
    segments: SkeletonDataComponent

    @classmethod
    def from_npy_paths(cls, npy_paths: FreemocapDataPaths) -> Self:
        return cls(
            total_body_center_of_mass=SkeletonDataComponent.from_segment(
                data=np.load(npy_paths.center_of_mass.total_body_center_of_mass),
                component_type=ComponentType.FULL_BODY_CENTER_OF_MASS,
                tracker_source=TrackerSourceType.CENTER_OF_MASS),

            segments=SkeletonDataComponent.from_segment(data=np.load(npy_paths.center_of_mass.segments),
                                                        component_type=ComponentType.SEGMENT_CENTER_OF_MASS,
                                                        tracker_source=TrackerSourceType.CENTER_OF_MASS)
        )
