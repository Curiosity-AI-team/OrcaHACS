Below is an **end-to-end example** showing how you can build a **HACS custom integration** (in `custom_components/orca_dev`) that:

1. Runs a simple HTTP endpoint (server) inside Home Assistant to receive text from an external script (which you’ve described uses FastAPI, but any HTTP client would work).  
2. Forwards the received text to **Home Assistant Assist** (i.e., the `conversation.process` service).

This setup will let you send text from an external Python script (e.g., `scripts/test_request.py`) to your custom integration endpoint inside Home Assistant. The integration will then relay that text to the built-in **Assist** feature.

---

## 1. File/Folder Structure

A minimal structure for your custom integration looks like this:

```
config/
├── custom_components/
│   └── orca_dev/
│       ├── __init__.py
│       └── manifest.json
└── scripts/
    └── test_request.py
```

> **Notes**  
> - Replace `config/` with the actual path to your Home Assistant config folder (often `~/.homeassistant` or `/config` in Docker).  
> - `test_request.py` is your external FastAPI (or any HTTP client) script that sends text to Home Assistant.

---

## 2. `manifest.json` (in `custom_components/orca_dev/`)

Create `manifest.json` with the basic metadata for your custom integration:

```json
{
  "domain": "orca_dev",
  "name": "Orca Dev Integration",
  "version": "0.0.1",
  "documentation": "https://github.com/yourusername/orca_dev",
  "requirements": [],
  "dependencies": [],
  "codeowners": [],
  "iot_class": "local_polling"
}
```

**Key fields**:

- **domain**: Must match the folder name (`orca_dev`).  
- **name**: A human-readable name for your integration.  
- **version**: Required by Home Assistant for custom integrations.  
- **documentation**: (Optional) but recommended for HACS listing.  

---

## 3. `__init__.py` (in `custom_components/orca_dev/`)

Below is a minimal example showing how to:

1. Register an **HTTP endpoint** (using Home Assistant’s built-in `aiohttp` server).  
2. Receive JSON data (`text`) from a POST request.  
3. Call the `conversation.process` service to feed the text into **Home Assistant Assist**.

```python
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)

DOMAIN = "orca_dev"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the orca_dev integration (YAML-based)."""
    hass.http.register_view(OrcaDevReceiveView())
    _LOGGER.info("orca_dev integration is set up and HTTP view is registered.")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the orca_dev integration from UI config entries (if implemented)."""
    # If you implement a config flow, you would initialize your integration here.
    hass.http.register_view(OrcaDevReceiveView())
    _LOGGER.info("orca_dev integration is set up via config entry and HTTP view is registered.")
    return True


class OrcaDevReceiveView(HomeAssistantView):
    """Expose a simple POST endpoint for receiving text and sending it to HA Assist."""

    url = "/api/orca_dev/receive_text"   # URL path to POST to
    name = "api:orca_dev:receive_text"   # Name used internally
    requires_auth = False                # Set to True if you require authentication

    async def post(self, request):
        """Handle POST requests to receive JSON and forward text to conversation.process."""
        hass = request.app["hass"]

        try:
            data = await request.json()
            text = data.get("text", "")
            if not text:
                return self.json({"error": "No 'text' key found in JSON"}, status=400)

            _LOGGER.info("Received text from external script: %s", text)

            # Call the conversation service to inject text into Assist
            await hass.services.async_call(
                "conversation",
                "process",
                {"text": text},
                blocking=False,
            )

            return self.json({"status": "ok", "received_text": text})

        except Exception as err:
            _LOGGER.error("Error in orca_dev endpoint: %s", err)
            return self.json({"error": str(err)}, status=500)
```

### Key Points in `__init__.py`

- **`hass.http.register_view(OrcaDevReceiveView())`**: This adds a new route (`/api/orca_dev/receive_text`) to Home Assistant’s internal web server.
- **`requires_auth = False`**:  
  - If you set this to `True`, your external script must supply an auth token (long-lived token or otherwise).  
  - If you leave it `False`, the endpoint is open (only recommended in a secure local environment).
- **Calling the conversation service**:  
  ```python
  await hass.services.async_call(
      "conversation", "process", {"text": text}, blocking=False
  )
  ```
  This is the key step that **injects** the text into Home Assistant’s Assist engine.

---

## 4. External Script: `test_request.py`

This script **acts as a client**. It will send a POST request to the custom integration endpoint we created above.

### 4A. Using `requests` (simplest example)

```python
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
```

### 4B. Using FastAPI (if you prefer an async client)

If your script is actually a FastAPI app calling Home Assistant, you might do something like:

```python
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
```

Then you can POST to **your** FastAPI app (e.g., `http://localhost:8000/send_text/`) with a JSON body like `{"text": "Hello from external script"}` and it will forward to Home Assistant.

---

## 5. Installing as a HACS Custom Repository (Optional)

If you want to distribute or install this integration via HACS:

1. Push the `custom_components/orca_dev` folder to its own public GitHub repository.  
2. In Home Assistant > **HACS** > **Integrations** > **...** (three dots menu) > **Custom repositories**:
   - Add your GitHub repo URL.
   - Select **Integration**.
   - Click **Add**.
3. The next time you open HACS > **Integrations**, your `orca_dev` integration should appear under “**Custom Repositories**” to install.

---

## 6. Testing the Flow

1. **Restart Home Assistant** so that it loads your new custom integration.  
2. Look for **orca_dev** logs in Developer Tools > Logs. You should see:
   ```
   [custom_components.orca_dev] orca_dev integration is set up and HTTP view is registered.
   ```
3. Run `test_request.py` (or your FastAPI script) to send `"Hello from my external script!"` to `/api/orca_dev/receive_text`.
4. In Home Assistant, check:
   - **Developer Tools > Logs** for the incoming text log.  
   - **Assist** to see if it received the text as if a user typed it in the conversation.

---

## 7. Security Considerations

- **Authentication**:  
  If your Home Assistant instance is open beyond a secure LAN, set `requires_auth = True` and pass a valid **Bearer token** in the header from your external script.  
- **TLS/HTTPS**:  
  If needed, proxy requests through an HTTPS front-end like Nginx or Caddy.

---

## Summary

- **Custom Integration** (`orca_dev`): Registers a POST endpoint in Home Assistant that accepts JSON, extracts `"text"`, and feeds it to the **conversation.process** (Assist) service.  
- **External Script**: Sends HTTP POST requests (with or without FastAPI) to that endpoint.  
- **Result**: You can seamlessly push text from any external code into Home Assistant’s Assist feature for further automation or interpretation.

Feel free to adapt the example to your specific needs—whether you’re using **FastAPI** as a client, adding more complex logic, or requiring authentication tokens for secure setups. 

Enjoy building your custom integration! If you have more questions about advanced config flows, authentication, or add-on development, let me know.