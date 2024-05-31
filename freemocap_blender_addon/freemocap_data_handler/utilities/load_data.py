from freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler


def load_freemocap_data(
        recording_path: str,
) -> FreemocapDataHandler:
    print(f"Loading freemocap_data from {recording_path}....")

    try:
        handler = create_freemocap_data_handler(recording_path=recording_path)
        print(f"Loaded freemocap_data from {recording_path} successfully: \n{handler}")

    except Exception as e:
        print(f"Failed to load freemocap freemocap_data: {e}")
        print(e)
        raise e

    return handler
