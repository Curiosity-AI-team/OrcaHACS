orca_bridge:
  icon: mdi:server


curl -X POST "http://127.0.0.1:8123/api/orca_bridge/receive_text" -H "Content-Type: application/json" -d '{"text": "Hello", "battery": 90}