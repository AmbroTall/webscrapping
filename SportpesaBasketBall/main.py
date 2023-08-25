import asyncio
import websockets


async def connect_websocket():
    uri = "wss://example.com/websocket"  # Replace with the WebSocket server URL

    async with websockets.connect(uri) as websocket:
        # Perform any required authentication or setup

        while True:
            # Wait for incoming messages
            message = await websocket.recv()

            # Process the received message
            print("Received message:", message)

            # Perform any further data processing or actions based on the received data


# Run the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_websocket())
