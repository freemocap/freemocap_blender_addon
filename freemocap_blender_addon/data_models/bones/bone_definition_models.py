import math
from dataclasses import dataclass, field

import numpy as np


@dataclass
class BoneDefinition:
    head: str
    tail: str

@dataclass
class BoneStatistics:
    name: str
    definition: BoneDefinition
    lengths: list[float] = field(default_factory=list)  # List of bone lengths
    _mean: float = None
    _median: float = None
    _standard_deviation: float = None
    _median_absolute_deviation: float = None

    @property
    def mean(self):
        if self._mean is None and len(self.lengths) > 0:
            self._mean = np.nanmean(np.array(self.lengths))
        return self._mean

    @property
    def median(self):
        if self._median is None and len(self.lengths) > 0:
            self._median = np.nanmedian(np.array(self.lengths))
        return self._median

    @property
    def standard_deviation(self):
        if self._standard_deviation is None and len(self.lengths) > 0:
            self._standard_deviation = np.nanstd(np.array(self.lengths))
        return self._standard_deviation

    @property
    def median_absolute_deviation(self):
        if self._median_absolute_deviation is None and len(self.lengths) > 0:
            self._median_absolute_deviation = np.nanmean(
                np.array([np.abs(length - self.mean) for length in self.lengths if not math.isnan(length)])
            )
        return self._median_absolute_deviation

    @property
    def coefficient_of_variation_std(self):
        if self.mean is None or self.standard_deviation is None or self.mean == 0 or len(self.lengths) == 0:
            return None
        return self.standard_deviation / self.mean

    @property
    def coefficient_of_variation_mad(self):
        if self.median is None or self.median_absolute_deviation is None or self.median == 0 or len(self.lengths) == 0:
            return None
        return self.median_absolute_deviation / self.median

    def as_dict(self):
        return {
            'name': self.name,
            'definition': self.definition.__dict__,
            'lengths': self.lengths,
            'mean': self.mean,
            'median': self.median,
            'standard_deviation': self.standard_deviation,
            'median_absolute_deviation': self.median_absolute_deviation,
            'coefficient_of_variation_std': self.coefficient_of_variation_std,
            'coefficient_of_variation_mad': self.coefficient_of_variation_mad
        }

    def as_short_keys_dict(self):
        return {
            'name': self.name,
           'mean': self.mean,
           'median': self.median,
           'std': self.standard_deviation,
            'mad': self.median_absolute_deviation,
            'cv_std': self.coefficient_of_variation_std,
            'cv_mad': self.coefficient_of_variation_mad

        }
    def as_row(self):
        return list()

    def as_fixed_width_string(self, width=10):
        return "".join([f"{str(value):<{width}}" for value in self.as_row()])

    def as_fixed_width_string_header(self, width=10):
        return "".join([f"{str(key):<{width}}" for key in self.as_short_keys_dict().keys()])