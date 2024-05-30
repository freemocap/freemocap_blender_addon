import pytest
import numpy as np
from typing import List
from message import CentralTendencyMeasures, VariabilityMeasures, SampleStatistics


@pytest.fixture
def sample_data() -> Samples:
    return [1.0, 2.0, 3.0, 4.0, 5.0]

@pytest.fixture
def sample_ndarray(sample_data: Samples) -> np.ndarray:
    return np.array(sample_data)

def test_central_tendency_measures_from_data(sample_ndarray: np.ndarray) -> None:
    ctm = CentralTendencyMeasures.from_data(sample_ndarray)
    assert ctm.mean == np.nanmean(sample_ndarray)
    assert ctm.median == np.nanmedian(sample_ndarray)

def test_central_tendency_measures_from_samples(sample_data: Samples) -> None:
    ctm = CentralTendencyMeasures.from_samples(sample_data)
    assert ctm.mean == np.nanmean(sample_data)
    assert ctm.median == np.nanmedian(sample_data)

def test_variability_measures_from_ndarray(sample_ndarray: np.ndarray) -> None:
    vm = VariabilityMeasures.from_ndarray(sample_ndarray)
    assert vm.stddev == np.nanstd(sample_ndarray)
    assert vm.mad == np.nanmedian(np.abs(sample_ndarray - np.nanmedian(sample_ndarray)))
    assert vm.iqr == np.nanpercentile(sample_ndarray, 75) - np.nanpercentile(sample_ndarray, 25)
    assert vm.ci95 == 1.96 * np.nanstd(sample_ndarray) / np.sqrt(len(sample_ndarray))

def test_variability_measures_from_samples(sample_data: Samples) -> None:
    vm = VariabilityMeasures.from_samples(sample_data)
    assert vm.stddev == np.nanstd(sample_data)
    assert vm.mad == np.nanmedian(np.abs(sample_data - np.nanmedian(sample_data)))
    assert vm.iqr == np.nanpercentile(sample_data, 75) - np.nanpercentile(sample_data, 25)
    assert vm.ci95 == 1.96 * np.nanstd(sample_data) / np.sqrt(len(sample_data))

def test_sample_statistics_properties(sample_data: Samples) -> None:
    stats = SampleStatistics(np.array(sample_data))
    assert stats.samples == sample_data
    assert stats.number_of_samples == len(sample_data)
    assert isinstance(stats.measures_of_central_tendency, CentralTendencyMeasures)
    assert isinstance(stats.measures_of_variability, VariabilityMeasures)

def test_sample_statistics_delegation(sample_data: Samples) -> None:
    stats = SampleStatistics(np.array(sample_data))
    assert stats.mean == np.nanmean(sample_data)
    assert stats.median == np.nanmedian(sample_data)
    assert stats.stddev == np.nanstd(sample_data)
    assert stats.mad == np.nanmedian(np.abs(sample_data - np.nanmedian(sample_data)))
    assert stats.iqr == np.nanpercentile(sample_data, 75) - np.nanpercentile(sample_data, 25)
    assert stats.ci95 == 1.96 * np.nanstd(sample_data) / np.sqrt(len(sample_data))

def test_empty_data() -> None:
    with pytest.raises(ValueError, match="Sample list cannot be empty"):
        CentralTendencyMeasures.from_data(np.array([]))
    with pytest.raises(ValueError, match="Sample list cannot be empty"):
        CentralTendencyMeasures.from_samples([])
    with pytest.raises(ValueError, match="Sample list cannot be empty"):
        VariabilityMeasures.from_ndarray(np.array([]))
    with pytest.raises(ValueError, match="Sample list cannot be empty"):
        VariabilityMeasures.from_samples([])

def test_invalid_data_shape() -> None:
    with pytest.raises(ValueError, match="Sample list must be one-dimensional"):
        CentralTendencyMeasures.from_data(np.array([[1.0, 2.0], [3.0, 4.0]]))
    with pytest.raises(ValueError, match="Sample list must be one-dimensional"):
        CentralTendencyMeasures.from_samples([[1.0, 2.0], [3.0, 4.0]])
    with pytest.raises(ValueError, match="Sample list must be one-dimensional"):
        VariabilityMeasures.from_ndarray(np.array([[1.0, 2.0], [3.0, 4.0]]))
    with pytest.raises(ValueError, match="Sample list must be one-dimensional"):
        VariabilityMeasures.from_samples([[1.0, 2.0], [3.0, 4.0]])