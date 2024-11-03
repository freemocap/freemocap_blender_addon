import logging
import time

from skellyblender.core.client.http_client import HTTPClient
from skellyblender.core.client.websocket_client import WebSocketClient

logger = logging.getLogger(__name__)

PROTOCOL = "http"
HOSTNAME = "localhost"
PORT = 8005
APP_URL = f"{PROTOCOL}://{HOSTNAME}:{PORT}"

class FreemocapClient:
    def __init__(self, base_url: str = APP_URL):
        super().__init__()
        self._http_client = HTTPClient(base_url=base_url)
        self._ws_client = WebSocketClient(base_url=base_url)

    @property
    def http_client(self) -> HTTPClient:
        return self._http_client

    @property
    def websocket_client(self) -> WebSocketClient:
        return self._ws_client

    def connect_websocket(self):
        logger.debug("Client sending request to connect to WebSocket")
        self._ws_client.connect_websocket()

    def detect_cameras(self):
        logger.debug("Calling `cameras/detect` endpoint")
        self._http_client.get("/cameras/detect")

    def close_cameras(self):
        logger.debug("Calling `cameras/close` endpoint")
        self._http_client.get("/cameras/close")

    def shutdown_server(self) -> None:
        logger.debug("Calling `/app/shutdown` endpoint")
        self._http_client.get("/app/shutdown")
        self._http_client.close()
        self._ws_client.close()

    def start_recording(self):
        logger.debug("Calling `/cameras/record/start` endpoint")
        self._http_client.get("/cameras/record/start")

    def stop_recording(self):
        logger.debug("Calling `/cameras/record/stop` endpoint")
        self._http_client.get("/cameras/record/stop")

    # def detect_and_connect_to_cameras(self):
    #     logger.debug("Calling `cameras/connect` endpoint")
    #
    #     self._http_client.get("/cameras/connect/detect")

    def apply_settings_to_cameras(self, camera_configs):
        logger.debug("Calling `/cameras/connect/apply` endpoint")
        if not camera_configs:
            raise ValueError("CameraConfigs are `None`")
        data = {camera_id: config.model_dump() for camera_id, config in camera_configs.items()}
        self._http_client.post(endpoint="/cameras/connect/apply",
                               data=data)

if __name__ == "__main__":
    demo_client = FreemocapClient()
    try:
        demo_client.connect_websocket()
        demo_client.detect_cameras()
        demo_client.start_recording()
        time.sleep(5)
        demo_client.stop_recording()
        demo_client.close_cameras()
    finally:
        demo_client.shutdown_server()



