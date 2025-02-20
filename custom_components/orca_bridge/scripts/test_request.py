#!/usr/bin/env python3

import requests

BASE_URL = "http://127.0.0.1:8123"  # Adjust if HA is on a different IP/port

def send_text_to_ha(text):
    url = f"{BASE_URL}/api/orca_dev/receive_text"
    payload = {"text": text}
    # If 'requires_auth = True' in your integration, include a Bearer token:
    # headers = {"Authorization": "Bearer YOUR_LONG_LIVED_TOKEN"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Example usage:
    result = send_text_to_ha("Hello from my external script!")
    print("Response from orca_dev integration:", result)