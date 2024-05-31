from dataclasses import dataclass
from typing import List, Union
import numpy as np

Z_SCORE_95_CI = 1.96  # Z-score for 95% confidence interval

SampleList = List[Union[float, int]]  # custom type alias for a list of numerical samples

def validate_samples(data: np.ndarray) -> None:
    """ Validate the input sample data. """
    if data.size == 0:
        raise ValueError("Sample list cannot be empty")
    if data.ndim != 1:
        raise ValueError("Sample list must be one-dimensional")
    if np.all(np.isnan(data)):
        raise ValueError("Sample list cannot contain only NaN values")
    if np.all(np.isinf(data)):
        raise ValueError("Sample list cannot contain only infinite values")
    if not np.issubdtype(data.dtype, np.number):
        raise ValueError("Sample list must contain only numerical values")

@dataclass
class SampleData:
    data: np.ndarray

    def __post_init__(self):
        validate_samples(self.data)

    @classmethod
    def from_samples(cls, samples: SampleList) -> 'SampleData':
        return cls(data=np.array(samples))

    @property
    def samples(self) -> SampleList:
        return self.data.tolist()

    @property
    def number_of_samples(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f"SampleData(data={self.data.shape})"

@dataclass
class CentralTendencyMeasures:
    mean: float
    median: float

    @classmethod
    def from_samples(cls, samples: SampleList) -> 'CentralTendencyMeasures':
        data = np.array(samples)
        validate_samples(data)
        return cls(
            mean=np.nanmean(data),
            median=np.nanmedian(data),
        )

@dataclass
class VariabilityMeasures:
    stddev: float
    mad: float
    iqr: float
    ci95: float

    @classmethod
    def from_samples(cls, samples: SampleList) -> 'VariabilityMeasures':
        data = np.array(samples)
        validate_samples(data)
        return cls(
            stddev=np.nanstd(data),
            mad=np.nanmedian(np.abs(data - np.nanmedian(data))),
            iqr=np.nanpercentile(data, 75) - np.nanpercentile(data, 25),
            ci95=Z_SCORE_95_CI * np.nanstd(data) / np.sqrt(data.size),
        )

@dataclass
class DescriptiveStatistics:
    sample_data: SampleData

    @classmethod
    def from_samples(cls, samples: SampleList) -> 'DescriptiveStatistics':
        return cls(sample_data=SampleData.from_samples(samples))

    @property
    def samples(self) -> SampleList:
        return self.sample_data.samples

    @property
    def measures_of_central_tendency(self) -> CentralTendencyMeasures:
        return CentralTendencyMeasures.from_samples(self.samples)

    @property
    def measures_of_variability(self) -> VariabilityMeasures:
        return VariabilityMeasures.from_samples(self.samples)

    @property
    def data(self) -> np.ndarray:
        return self.sample_data.data

    @property
    def mean(self) -> float:
        return self.measures_of_central_tendency.mean

    @property
    def median(self) -> float:
        return self.measures_of_central_tendency.median

    @property
    def stddev(self) -> float:
        return self.measures_of_variability.stddev

    @property
    def mad(self) -> float:
        return self.measures_of_variability.mad

    @property
    def iqr(self) -> float:
        return self.measures_of_variability.iqr

    @property
    def ci95(self) -> float:
        return self.measures_of_variability.ci95

    @property
    def number_of_samples(self) -> int:
        return self.sample_data.number_of_samples

    def __str__(self) -> str:
        return (
            f"Descriptive Statistics:\n"
            f"\tNumber of Samples: {self.number_of_samples}\n"
            f"\tMean: {self.mean:.3f}\n"
            f"\tMedian: {self.median:.3f}\n"
            f"\tStandard Deviation: {self.stddev:.3f}\n"
            f"\tMedian Absolute Deviation: {self.mad:.3f}\n"
            f"\tInterquartile Range: {self.iqr:.3f}\n"
            f"\t95% Confidence Interval: ±{self.ci95:.3f}\n"
        )

if __name__ == "__main__":
    dummy_samples = [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = DescriptiveStatistics.from_samples(dummy_samples)

    print(stats)