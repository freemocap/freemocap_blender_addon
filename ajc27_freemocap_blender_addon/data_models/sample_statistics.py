from dataclasses import dataclass
from typing import List

import numpy as np

Z_SCORE_95_CI = 1.96  # Z-score for 95% confidence interval
Z_SCORE_99_CI = 2.58  # Z-score for 99% confidence interval

SampleList = List[float]  # custom type alias for a list of float samples


@dataclass
class SampleData:
    name: str
    data: np.ndarray

    def __post_init__(self):
        if self.data:
            raise ValueError("Sample list cannot be empty")
        if len(self.data.shape) != 1:
            raise ValueError("Sample list must be one-dimensional (for now)")
        if not np.any(self.data):
            raise ValueError("Sample list cannot be empty")
        if np.all(np.isnan(self.data)):
            raise ValueError("Sample list cannot contain only NaN values")
        if np.all(np.isinf(self.data)):
            raise ValueError("Sample list cannot contain only infinite values")
        if not np.issubdtype(self.data.dtype, np.number):
            raise ValueError("Sample list must contain only numerical values")

    @classmethod
    def from_samples(cls,
                     name: str,
                     samples: SampleList) -> 'SampleData':
        return cls(
            name=name,
            data=np.array(samples)
        )
    @property
    def samples(self) -> SampleList:
        return self.data.tolist()

    @property
    def number_of_samples(self) -> int:
        return len(self.samples)

    def __repr__(self) -> str:
        return f"SampleData(data={self.data.shape})"


@dataclass
class CentralTendencyMeasures:
    mean: float  # Arithmetic mean, simplest measure of central tendency
    median: float  # Middle value of a dataset, robust to outliers

    @classmethod
    def from_data(cls,
                  data: np.ndarray) -> 'CentralTendencyMeasures':
        return cls(
            mean=np.nanmean(data),
            median=np.nanmedian(data),
        )

    @classmethod
    def from_samples(cls,
                     samples: SampleList) -> 'CentralTendencyMeasures':
        if not samples:
            raise ValueError("Sample list cannot be empty")
        data = np.array(samples)
        if len(data.shape) != 1:
            raise ValueError("Sample list must be one-dimensional")

        return cls.from_data(data=data)


@dataclass
class VariabilityMeasures:
    """
    Class for measuring variability in a dataset.
    """
    stddev: float  # Standard deviation, measures the dispersion of a dataset
    mad: float  # Median absolute deviation, robust to outliers
    iqr: float  # Interquartile range, robust measure of dispersion
    ci95: float  # 95% confidence interval, range within which the true population mean is expected to lie

    @classmethod
    def from_ndarray(cls,
                     name: str,
                     data: np.ndarray) -> 'VariabilityMeasures':
        if not data:
            raise ValueError("Sample list cannot be empty")
        if len(data.shape) != 1:
            raise ValueError("Sample list must be one-dimensional")
        return cls(
            stddev=np.nanstd(data),
            mad=np.nanmedian(np.abs(data - np.nanmedian(data))),
            iqr=np.nanpercentile(data, 75) - np.nanpercentile(data, 25),
            ci95=Z_SCORE_95_CI * np.nanstd(data) / np.sqrt(len(data)),
        )

    @classmethod
    def from_samples(cls,
                     name: str,
                     samples: SampleList) -> 'VariabilityMeasures':
        if not samples:
            raise ValueError("Sample list cannot be empty")
        return cls.from_ndarray(
            name=name,
            data=np.array(samples))


@dataclass
class DescriptiveStatistics:
    """
    Descriptive statistics for a univariate measurement, such as a body segment length.
    "Univariate" means that there is only one variable being measured (i.e. the length of a body segment).
    """
    sample_data: SampleData

    @classmethod
    def from_samples(cls,
                        name: str,
                        samples: SampleList) -> 'DescriptiveStatistics':
            return cls(
                sample_data=SampleData.from_samples(name=name, samples=samples)
            )
    @property
    def samples(self) -> SampleList:
        return self.data.tolist()

    @property
    def measures_of_central_tendency(self) -> CentralTendencyMeasures:
        return CentralTendencyMeasures.from_samples(self.samples)

    @property
    def measures_of_variability(self) -> VariabilityMeasures:
        return VariabilityMeasures.from_samples(self.samples)

    def __getattr__(self, name: str) -> float:
        """
        Delegate attribute access to the appropriate component class.
        e.g, so that `self.mean` returns `self.measures_of_central_tendency.mean`
        """
        central_tendency = self.measures_of_central_tendency
        variability = self.measures_of_variability

        if hasattr(central_tendency, name):
            return getattr(central_tendency, name)
        elif hasattr(variability, name):
            return getattr(variability, name)
        else:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute '{name}'")


if __name__ == "__main__":
    samples = [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = DescriptiveStatistics(sample_data=SampleData(name="test", data=np.array(samples)))

    print(stats.mean)  # Accessing mean from CentralTendencyMeasures
    print(stats.stddev)  # Accessing stddev from VariabilityMeasures
