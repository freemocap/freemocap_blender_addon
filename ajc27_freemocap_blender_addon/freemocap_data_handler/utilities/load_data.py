from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.get_or_create_freemocap_data_handler import create_freemocap_data_handler
from ajc27_freemocap_blender_addon.system.configure_logging.configure_logging import LogStrings


def load_freemocap_data(
        recording_path: str,
) -> FreemocapDataHandler:
    print(f"{LogStrings.INFO} Loading freemocap_data from {recording_path}....")

    try:
        handler = create_freemocap_data_handler(recording_path=recording_path)
        print(f"{LogStrings.DEBUG} Loaded freemocap_data from {recording_path} successfully: \n{handler}")
        handler.mark_processing_stage("original_from_file")
    except Exception as e:
        print(f"{LogStrings.ERROR} Failed to load freemocap freemocap_data: {e}")
        print(LogStrings.ERROR, e)
        raise e

    return handler
