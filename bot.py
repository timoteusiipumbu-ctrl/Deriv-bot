import asyncio
import json
import websockets

# Deriv WebSocket API Endpoint (App ID 1089 is Deriv's default public app ID)
DERIV_URL = "wss://ws.derivws.com/websockets/v3?app_id=1089"

async def main():
    print("Starting Deriv Trading Bot...")
    try:
        async with websockets.connect(DERIV_URL) as websocket:
            print("Successfully connected to Deriv WebSocket API!")
            
            # Send a ping request to confirm active connection
            await websocket.send(json.dumps({"ping": 1}))
            response = await websocket.recv()
            print(f"Server response: {response}")
            
            # Keep the service active on Render
            while True:
                await asyncio.sleep(60)
                await websocket.send(json.dumps({"ping": 1}))
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
