from dataclasses import dataclass
from typing import Self

import numpy as np

from freemocap_blender_addon.freemocap_data.freemocap_data_component import FreemocapDataComponent, ComponentType
from freemocap_blender_addon.freemocap_data.freemocap_data_paths import FreemocapDataPaths, TrackerSourceType


@dataclass
class CenterOfMassData:
    total_body_center_of_mass: FreemocapDataComponent
    segments: FreemocapDataComponent

    @classmethod
    def from_npy_paths(cls, npy_paths: FreemocapDataPaths) -> Self:
        return cls(
            total_body_center_of_mass=FreemocapDataComponent.create(
                data=np.load(npy_paths.center_of_mass.total_body_center_of_mass),
                component_type=ComponentType.FULL_BODY_CENTER_OF_MASS,
                data_source=TrackerSourceType.CENTER_OF_MASS),

            segments=FreemocapDataComponent.create(data=np.load(npy_paths.center_of_mass.segments),
                                                   component_type=ComponentType.SEGMENT_CENTER_OF_MASS,
                                                   data_source=TrackerSourceType.CENTER_OF_MASS)
        )
