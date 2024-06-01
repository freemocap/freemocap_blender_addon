import enum
import io
import zipfile
from dataclasses import dataclass
from pathlib import Path

import requests

TEST_FOLDER_NAME = "freemocap_test_data"
SAMPLE_FOLDER_NAME = "freemocap_sample_data"
FREEMOCAP_BASE_FOLDER_NAME = "freemocap_data"
RECORDING_SESSIONS_PATH = "recording_sessions"
FREEMOCAP_BASE_FOLDER = str(Path().home() / FREEMOCAP_BASE_FOLDER_NAME)
TEST_FOLDER_PATH = str(Path(FREEMOCAP_BASE_FOLDER) / RECORDING_SESSIONS_PATH / TEST_FOLDER_NAME)
SAMPLE_FOLDER_PATH = str(Path(FREEMOCAP_BASE_FOLDER) / RECORDING_SESSIONS_PATH / SAMPLE_FOLDER_NAME)

FIGSHARE_SAMPLE_ZIP_FILE_URL = "https://figshare.com/ndownloader/files/45797067"
FIGSHARE_TEST_ZIP_FILE_URL = "https://figshare.com/ndownloader/files/45797073"


@dataclass
class ExampleData:
    url: str
    folder: str


class ExampleDataTypes(enum.Enum):
    SAMPLE: ExampleData = ExampleData(url=FIGSHARE_SAMPLE_ZIP_FILE_URL, folder=SAMPLE_FOLDER_PATH)
    TEST: ExampleData = ExampleData(url=FIGSHARE_TEST_ZIP_FILE_URL, folder=TEST_FOLDER_PATH)


def get_test_data_path(test_data_type: ExampleDataTypes = ExampleDataTypes.TEST) -> str:
    if not Path(test_data_type.value.folder).exists():
        download_example_data(**test_data_type.value.__dict__)

    return test_data_type.value.folder


def get_example_data_path(example_data_type: ExampleDataTypes) -> str:
    if not Path(example_data_type.value.folder).exists():
        download_example_data(**example_data_type.value.__dict__)
    return example_data_type.value.folder


def download_example_data(url: str, folder: str = FREEMOCAP_BASE_FOLDER_NAME) -> str:
    try:
        print(f"Downloading example data from {url} to {folder}...")

        r = requests.get(url, stream=True, timeout=(5, 60))
        r.raise_for_status()  # Check if request was successful

        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(folder)

        print(f"Sample data extracted to {str(folder)}")
        return folder

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise e
    except zipfile.BadZipFile as e:
        print(f"Failed to unzip the file: {e}")
        raise e


if __name__ == "__main__":
    outer_test_data_path = get_example_data_path(ExampleDataTypes.TEST)
    print(f"Example found/downloaded at {outer_test_data_path}")
