import os

LISTEN_ADDRESS = os.getenv("LISTEN_ADDRESS", "127.0.0.1")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8000"))

SCAN_FREQUENCY = int(os.getenv("SCAN_FREQUENCY", "900")) # How often we should scan for BLE advertisements (seconds)
SCAN_DURATION = int(os.getenv("SCAN_DURATION", "15")) # How long each scan should last (seconds)