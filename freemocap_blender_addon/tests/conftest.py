from pathlib import Path

import numpy as np
import pytest

from freemocap_blender_addon.experiments.named_ndarray import NamedNdarray
from freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths import FreemocapDataPaths
from freemocap_blender_addon.utilities.download_test_data import get_test_data_path, TEST_FOLDER_PATH


@pytest.fixture()
def recording_path_fixture() -> str:
    test_recording_path = get_test_data_path()
    assert Path(test_recording_path).exists()
    assert test_recording_path == TEST_FOLDER_PATH
    assert Path(Path(test_recording_path) / 'output_data').exists()
    return test_recording_path

@pytest.fixture
def freemocap_data_paths_fixture(recording_path_fixture: str) -> FreemocapDataPaths:
    paths: FreemocapDataPaths = FreemocapDataPaths.from_recording_path(path=recording_path_fixture)
    assert isinstance(paths, FreemocapDataPaths)
    return paths

@pytest.fixture(params=[np.uint8, np.uint16, np.uint32, np.uint64,
                        np.int8, np.int16, np.int32, np.int64,
                        np.float16, np.float32, np.float64,
                        bool, int, float,
                        # TODO - add weird types
                        # np.complex64, np.complex128,
                        # complex, str, bytes, np.void
                        ])

def dtype_fixture(request: pytest.FixtureRequest) -> np.dtype:
    return request.param


@pytest.fixture(params=[1, 2, 3, 4])
def number_of_dimensions_fixture(request: pytest.FixtureRequest) -> int:
    return request.param


@pytest.fixture(params=[1, 2, 3, 10])
def number_of_elements_fixture(request: pytest.FixtureRequest) -> int:
    return request.param


@pytest.fixture()
def array_shape_fixture(number_of_dimensions_fixture: int, number_of_elements_fixture: int) -> tuple:
    return tuple([number_of_elements_fixture] * number_of_dimensions_fixture)


@pytest.fixture()
def filled_array_fixture(array_shape_fixture: tuple, dtype_fixture: np.dtype) -> np.ndarray:
    if np.issubdtype(dtype_fixture, np.integer):
        return np.random.randint(0, 100, size=array_shape_fixture, dtype=dtype_fixture)
    elif np.issubdtype(dtype_fixture, np.floating):
        return np.random.uniform(0.0, 1.0, size=array_shape_fixture).astype(dtype_fixture)
    elif dtype_fixture == bool:
        return np.random.choice([False, True], size=array_shape_fixture)
    else:
        raise TypeError(f"Unsupported dtype: {dtype_fixture}")


@pytest.fixture()
def zeros_array_fixture(array_shape_fixture: tuple) -> np.ndarray:
    return np.zeros(array_shape_fixture)


@pytest.fixture()
def ones_array_fixture(array_shape_fixture: tuple) -> np.ndarray:
    return np.ones(array_shape_fixture)


@pytest.fixture(params=[1, 10, 49, 50, 51, 99, 100])
def number_of_nan_elements_fixture(random_array_fixture: np.ndarray, request: pytest.fixture) -> int:
    """
    replace a percentage of the array with np.nan
    """
    number_of_elements = random_array_fixture.size
    target_number_of_nan_elements = int(number_of_elements * request.param / 100)

    for _ in range(target_number_of_nan_elements):
        index = np.random.randint(0, number_of_elements)
        while random_array_fixture.flat[index] == np.nan:
            index = np.random.randint(0, number_of_elements)
        random_array_fixture.flat[index] = np.nan
    return target_number_of_nan_elements


@pytest.fixture()
def empty_array_fixture(array_shape_fixture: tuple) -> np.ndarray:
    return np.empty(array_shape_fixture, None)


@pytest.fixture()
def named_numpy_array_fixture(random_array_fixture: np.ndarray) -> NamedNdarray:
    return NamedNdarray(data=random_array_fixture, name="test_array")
