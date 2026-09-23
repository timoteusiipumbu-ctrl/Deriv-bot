import asyncio
import json
import os
import sys
import websockets

DERIV_TOKEN = os.environ.get("DERIV_TOKEN")
APP_ID = "1089"  # Default Deriv App ID
WS_URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"


async def ping_loop(websocket):
  """Sends ping every 30 seconds to keep connection alive."""
  while True:
    await asyncio.sleep(30)
    try:
      await websocket.send(json.dumps({"ping": 1}))
    except Exception:
      break


async def main():
  if not DERIV_TOKEN:
    print("ERROR: DERIV_TOKEN environment variable is missing!", flush=True)
    sys.exit(1)

  print("Starting Deriv Trading Bot...", flush=True)

  # Custom browser User-Agent header to prevent Cloudflare HTTP 520 rejection
  user_agent = (
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
      " like Gecko) Chrome/122.0.0.0 Safari/537.36"
  )

  try:
    async with websockets.connect(
        WS_URL, user_agent_header=user_agent
    ) as websocket:
      print(
          "Connected to Deriv WebSocket! Authorizing account...", flush=True
      )

      # Send authorization request
      await websocket.send(json.dumps({"authorize": DERIV_TOKEN}))

      # Start background ping process
      asyncio.create_task(ping_loop(websocket))

      async for message in websocket:
        data = json.loads(message)

        if data.get("msg_type") == "authorize":
          if "error" in data:
            print(
                f"Authorization error: {data['error']['message']}", flush=True
            )
            break
          auth_info = data["authorize"]
          print(
              f"Successfully Authorized! Account: {auth_info.get('email')} |"
              f" Balance: {auth_info.get('balance')}"
              f" {auth_info.get('currency')}",
              flush=True,
          )

        elif data.get("msg_type") == "ping":
          pass  # Ping acknowledgment received

  except Exception as e:
    print(f"Connection error: {e}", flush=True)


if __name__ == "__main__":
  asyncio.run(main())
