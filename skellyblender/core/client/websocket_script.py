import bpy
import asyncio
import websockets
from typing import NoReturn


async def connect_to_websocket(url: str) -> NoReturn:
    """Connect to the WebSocket server and receive messages.

    Parameters
    ----------
    url : str
        The WebSocket server URL.

    """
    async with websockets.connect(url) as websocket:
        print("Connected to the WebSocket server.")
        try:
            while True:
                message = await websocket.recv()
                print(f"Message received from server: {message}")
                # Implement your message handling logic here
        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")


def start_websocket_client(url: str) -> NoReturn:
    """Start the WebSocket client.

    Parameters
    ----------
    url : str
        The WebSocket server URL.

    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_to_websocket(url))


# Example usage
url = 'ws://localhost:8005/websocket/connect'
print(f"Connecting to WebSocket server at {url}...")
start_websocket_client(url)
print("Done.")
