
from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler

_FREEMOCAP_DATA_HANDLER = None


def get_or_create_freemocap_data_handler(recording_path: str):
    global _FREEMOCAP_DATA_HANDLER
    if _FREEMOCAP_DATA_HANDLER is None:
        _FREEMOCAP_DATA_HANDLER = FreemocapDataHandler.from_recording_path(recording_path=recording_path)
    return _FREEMOCAP_DATA_HANDLER


def create_freemocap_data_handler(recording_path: str):
    global _FREEMOCAP_DATA_HANDLER
    _FREEMOCAP_DATA_HANDLER = FreemocapDataHandler.from_recording_path(recording_path=recording_path)
    return _FREEMOCAP_DATA_HANDLER
