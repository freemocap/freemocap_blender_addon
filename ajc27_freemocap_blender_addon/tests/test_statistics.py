import numpy as np
import pytest

from ajc27_freemocap_blender_addon.data_models.sample_statistics import SampleList, CentralTendencyMeasures, \
    VariabilityMeasures, Des


@pytest.fixture
def sample_data_fixture() -> SampleList:
    return [1.0, 2.0, 3.0, 4.0, 5.0]


@pytest.fixture
def sample_ndarray_fixture(sample_data_fixture: SampleList) -> np.ndarray:
    return np.array(sample_data_fixture)


@pytest.fixture
def sample_statistics_fixture(sample_data_fixture: SampleList) -> Des:
    return Des.from_samples(sample_data_fixture)


def test_central_tendency_measures_from_data(sample_ndarray_fixture: np.ndarray) -> None:
    ctm = CentralTendencyMeasures.from_data(sample_ndarray_fixture)
    assert ctm.mean == np.nanmean(sample_ndarray_fixture)
    assert ctm.median == np.nanmedian(sample_ndarray_fixture)


def test_central_tendency_measures_from_samples(sample_data: SampleList) -> None:
    ctm = CentralTendencyMeasures.from_samples(sample_data)
    assert ctm.mean == np.nanmean(sample_data)
    assert ctm.median == np.nanmedian(sample_data)


def test_variability_measures_from_ndarray(sample_ndarray_fixture: np.ndarray) -> None:
    vm = VariabilityMeasures.from_ndarray(sample_ndarray_fixture)
    assert vm.stddev == np.nanstd(sample_ndarray_fixture)
    assert vm.mad == np.nanmedian(np.abs(sample_ndarray_fixture - np.nanmedian(sample_ndarray_fixture)))
    assert vm.iqr == np.nanpercentile(sample_ndarray_fixture, 75) - np.nanpercentile(sample_ndarray_fixture, 25)
    assert vm.ci95 == 1.96 * np.nanstd(sample_ndarray_fixture) / np.sqrt(len(sample_ndarray_fixture))


def test_variability_measures_from_samples(sample_data: SampleList) -> None:
    vm = VariabilityMeasures.from_samples(sample_data)
    assert vm.stddev == np.nanstd(sample_data)
    assert vm.mad == np.nanmedian(np.abs(sample_data - np.nanmedian(sample_data)))
    assert vm.iqr == np.nanpercentile(sample_data, 75) - np.nanpercentile(sample_data, 25)
    assert vm.ci95 == 1.96 * np.nanstd(sample_data) / np.sqrt(len(sample_data))


def test_sample_statistics_properties(sample_statistics_fixture: Des,
                                      sample_data: SampleList) -> None:
    stats = sample_statistics_fixture
    assert stats.samples == sample_data
    assert stats.number_of_samples == len(sample_data)
    assert isinstance(stats.measures_of_central_tendency, CentralTendencyMeasures)
    assert isinstance(stats.measures_of_variability, VariabilityMeasures)


def test_sample_statistics_delegation(sample_statistics_fixture: Des,
                                      sample_data: SampleList) -> None:
    stats = sample_statistics_fixture
    assert stats.mean == np.nanmean(sample_data)
    assert stats.median == np.nanmedian(sample_data)
    assert stats.stddev == np.nanstd(sample_data)
    assert stats.mad == np.nanmedian(np.abs(sample_data - np.nanmedian(sample_data)))
    assert stats.iqr == np.nanpercentile(sample_data, 75) - np.nanpercentile(sample_data, 25)
    assert stats.ci95 == 1.96 * np.nanstd(sample_data) / np.sqrt(len(sample_data))


def test_empty_data() -> None:
    try:  # note - avoid `pytest.raises` and similar bc they are not thread safe 🙄
        CentralTendencyMeasures.from_data(np.array([]))
    except ValueError as e:
        assert str(e) == "Sample list cannot be empty"

    try:
        CentralTendencyMeasures.from_samples([])
    except ValueError as e:
        assert str(e) == "Sample list cannot be empty"

    try:
        VariabilityMeasures.from_ndarray(np.array([]))
    except ValueError as e:
        assert str(e) == "Sample list cannot be empty"

    try:
        VariabilityMeasures.from_samples([])
    except ValueError as e:
        assert str(e) == "Sample list cannot be empty"


def test_invalid_data_shape() -> None:
    try:
        CentralTendencyMeasures.from_data(np.array([[1.0, 2.0], [3.0, 4.0]]))
    except ValueError as e:
        assert str(e) == "Sample list must be one-dimensional"

    try:
        CentralTendencyMeasures.from_samples([[1.0, 2.0], [3.0, 4.0]])
    except ValueError as e:
        assert str(e) == "Sample list must be one-dimensional"

    try:
        VariabilityMeasures.from_ndarray(np.array([[1.0, 2.0], [3.0, 4.0]]))
    except ValueError as e:
        assert str(e) == "Sample list must be one-dimensional"

    try:
        VariabilityMeasures.from_samples([[1.0, 2.0], [3.0, 4.0]])
    except ValueError as e:
        assert str(e) == "Sample list must be one-dimensional"
