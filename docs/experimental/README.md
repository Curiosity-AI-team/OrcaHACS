orca_bridge:
  icon: mdi:server

demo:


curl -X POST "http://127.0.0.1:8123/api/orca_bridge/receive_text" -H "Content-Type: application/json" -d '{"text": "Turn the AC on", "battery": 90}' | jq

curl -X POST "http://127.0.0.1:8123/api/orca_bridge/receive_text" -H "Content-Type: application/json" -d '{"text": "Weather", "battery": -1}' | jq

curl http://localhost:8123/api/orca_bridge/devices | jq


