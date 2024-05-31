import numpy as np
import pytest

from freemocap_blender_addon.models.sample_statistics import SampleList, CentralTendencyMeasures, \
    DescriptiveStatistics, VariabilityMeasures, SampleData


@pytest.fixture
def sample_data_fixture() -> SampleList:
    return [1.0, 2.0, 3.0, 4.0, 5.0]


@pytest.fixture
def sample_ndarray_fixture(sample_data_fixture: SampleList) -> np.ndarray:
    return np.array(sample_data_fixture)


@pytest.fixture
def sample_statistics_fixture(sample_data_fixture: SampleList) -> DescriptiveStatistics:
    return DescriptiveStatistics.from_samples(sample_data_fixture)


def test_central_tendency_measures_from_samples(sample_data_fixture: SampleList) -> None:
    ctm = CentralTendencyMeasures.from_samples(sample_data_fixture)
    assert ctm.mean == np.nanmean(sample_data_fixture)
    assert ctm.median == np.nanmedian(sample_data_fixture)


def test_variability_measures_from_samples(sample_data_fixture: SampleList) -> None:
    vm = VariabilityMeasures.from_samples(sample_data_fixture)
    assert vm.stddev == np.nanstd(sample_data_fixture)
    assert vm.mad == np.nanmedian(np.abs(sample_data_fixture - np.nanmedian(sample_data_fixture)))
    assert vm.iqr == np.nanpercentile(sample_data_fixture, 75) - np.nanpercentile(sample_data_fixture, 25)
    assert vm.ci95 == 1.96 * np.nanstd(sample_data_fixture) / np.sqrt(len(sample_data_fixture))


def test_sample_data_validation() -> None:
    correct_error = False
    try:  # note - not using `pytest.raises` here bc its not thread safe
        SampleData(data=np.array([]))
    except ValueError as e:
        correct_error = True
    assert correct_error
    correct_error = False

    try:
        SampleData(data=np.array([[1.0, 2.0], [3.0, 4.0]]))
    except ValueError as e:
        correct_error = True
    assert correct_error
    correct_error = False

    try:
        SampleData(data=np.array([np.nan, np.nan, np.nan]))
    except ValueError as e:
        correct_error = True
    assert correct_error

    try:
        SampleData(data=np.array([np.inf, -np.inf, np.inf]))
    except ValueError as e:
        correct_error = True
    assert correct_error


def test_invalid_data_shape() -> None:
    correct_error = False
    try:  # note - not using `pytest.raises` here bc its not thread safe
        CentralTendencyMeasures.from_samples([[1.0, 2.0], [3.0, 4.0]])
    except ValueError as e:
        correct_error = True
    assert correct_error
    correct_error = False
    try:
        VariabilityMeasures.from_samples([[1.0, 2.0], [3.0, 4.0]])
    except ValueError as e:
        correct_error = True
    assert correct_error


def test_descriptive_statistics(sample_statistics_fixture: DescriptiveStatistics) -> None:
    stats = sample_statistics_fixture
    assert stats.mean == np.nanmean(stats.samples)
    assert stats.median == np.nanmedian(stats.samples)
    assert stats.stddev == np.nanstd(stats.samples)
    assert stats.mad == np.nanmedian(np.abs(stats.samples - np.nanmedian(stats.samples)))
    assert stats.iqr == np.nanpercentile(stats.samples, 75) - np.nanpercentile(stats.samples, 25)
    assert stats.ci95 == 1.96 * np.nanstd(stats.samples) / np.sqrt(len(stats.samples))
    assert stats.number_of_samples == len(stats.samples)
