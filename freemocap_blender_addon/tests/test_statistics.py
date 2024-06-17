import numpy as np
import pytest

from freemocap_blender_addon.utilities.sample_statistics import CentralTendencyMeasures, \
    DescriptiveStatistics, VariabilityMeasures, SamplesType, SampleData


@pytest.fixture(params=[
    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    [1, 2, 3, 4, 5, 6],
    np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
    np.array([[1, 2, 3], [4, 5, 6]])
])
def samples_fixture(request) -> SamplesType:
    assert isinstance(request.param, (list, np.ndarray))
    return request.param


@pytest.fixture
def sample_data_fixture(samples_fixture: SamplesType) -> SampleData:
    return SampleData(data=samples_fixture)


@pytest.fixture
def sample_statistics_fixture(samples_fixture: SamplesType) -> DescriptiveStatistics:
    return DescriptiveStatistics.from_samples(samples_fixture)


def test_central_tendency_measures_from_samples(sample_data_fixture: SampleData) -> None:
    ctm = CentralTendencyMeasures.from_samples(samples=sample_data_fixture)
    assert ctm.mean == np.nanmean(sample_data_fixture.data)
    assert ctm.median == np.nanmedian(sample_data_fixture.data)


def test_variability_measures_from_samples(sample_data_fixture: SampleData) -> None:
    vm = VariabilityMeasures.from_samples(samples=sample_data_fixture)
    assert vm.standard_deviation == np.nanstd(sample_data_fixture.data)
    assert vm.mad == np.nanmedian(np.abs(sample_data_fixture.data - np.nanmedian(sample_data_fixture.data)))
    assert vm.iqr == np.nanpercentile(sample_data_fixture.data, 75) - np.nanpercentile(sample_data_fixture.data, 25)
    assert vm.ci95 == 1.96 * np.nanstd(sample_data_fixture.data) / np.sqrt(len(sample_data_fixture.data))


def test_sample_data_validation() -> None:
    with pytest.raises(ValueError):
        SampleData(data=np.array([]))

    with pytest.raises(ValueError):
        SampleData(data=np.array([np.nan, np.nan, np.nan]))

    with pytest.raises(ValueError):
        SampleData(data=np.array([np.inf, -np.inf, np.inf]))


def test_descriptive_statistics(sample_statistics_fixture: DescriptiveStatistics) -> None:
    stats = sample_statistics_fixture
    assert stats.mean == np.nanmean(stats.sample_data.data)
    assert stats.median == np.nanmedian(stats.sample_data.data)
    assert stats.standard_deviation == np.nanstd(stats.sample_data.data)
    assert stats.median_absolute_deviation == np.nanmedian(
        np.abs(stats.sample_data.data - np.nanmedian(stats.sample_data.data)))
    assert stats.interquartile_range == np.nanpercentile(stats.sample_data.data, 75) - np.nanpercentile(
        stats.sample_data.data, 25)
    assert stats.confidence_interval_95 == 1.96 * np.nanstd(stats.sample_data.data) / np.sqrt(
        len(stats.sample_data.data))
    assert stats.number_of_samples == len(stats.sample_data.data)
