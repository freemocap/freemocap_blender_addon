from pathlib import Path

from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.get_or_create_freemocap_data_handler import \
    create_freemocap_data_handler

_BASE_FREEMOCAP_RECORDINGS_PATH = Path().home() / "freemocap_data" / "recording_sessions"
_FREEMOCAP_TEST_DATA_PATH = _BASE_FREEMOCAP_RECORDINGS_PATH / "freemocap_test_data"
_FREEMOCAP_SAMPLE_DATA_PATH = _BASE_FREEMOCAP_RECORDINGS_PATH / "freemocap_sample_data"


def get_test_recording_path() -> str:
    if _FREEMOCAP_TEST_DATA_PATH.exists():
        return str(_FREEMOCAP_TEST_DATA_PATH)
    elif _FREEMOCAP_SAMPLE_DATA_PATH.exists():
        return str(_FREEMOCAP_SAMPLE_DATA_PATH)
    else:
        return ""


def load_freemocap_data(
        recording_path: str,
) -> FreemocapDataHandler:
    print(f"Loading freemocap_data from {recording_path}....")

    try:
        handler = create_freemocap_data_handler(recording_path=recording_path)
        print(f"Loaded freemocap_data from {recording_path} successfully: \n{handler}")
        handler.mark_processing_stage("original_from_file")
    except Exception as e:
        print(f"Failed to load freemocap freemocap_data: {e}")
        print(e)
        raise e

    return handler
