#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
import httpx  # async client

app = FastAPI()
BASE_URL = "http://127.0.0.1:8123"

@app.post("/send_text/")
async def send_text_endpoint(text: str):
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/api/orca_dev/receive_text"
        data = {"text": text}
        # If requires_auth=True in integration, add token:
        # headers = {"Authorization": "Bearer YOUR_LONG_LIVED_TOKEN"}
        headers = {"Content-Type": "application/json"}
        response = await client.post(url, json=data, headers=headers)
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)