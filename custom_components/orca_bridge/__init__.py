import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)
DOMAIN = "orca_bridge"

class OrcaDevReceiveView(HomeAssistantView):
    """Expose a POST endpoint for receiving text and system status updates."""
    url = "/api/orca_bridge/receive_text"
    name = "api:orca_bridge:receive_text"
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        try:
            data = await request.json()
            text = data.get("text", "")
            battery = data.get("battery", None)
            error_code = data.get("error_code", None)

            if not text:
                return self.json({"error": "Missing 'text' in JSON"}, status=400)

            if battery is not None:
                hass.data[DOMAIN]["battery"] = battery
            if error_code is not None:
                hass.data[DOMAIN]["last_error"] = error_code

            _LOGGER.info(f"Received text: {text}, Battery: {battery}, Error Code: {error_code}")

            await hass.services.async_call(
                "conversation",
                "process",
                {"text": text},
                blocking=False,
            )

            return self.json({"status": "ok", "received_text": text})
        except Exception as err:
            _LOGGER.error("Error in orca_bridge API: %s", err)
            return self.json({"error": str(err)}, status=500)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the orca_bridge integration via YAML."""
    hass.http.register_view(OrcaDevReceiveView())
    _LOGGER.info("orca_bridge integration (YAML) is set up and HTTP view is registered.")
    # Initialize integration data
    hass.data.setdefault(DOMAIN, {"battery": 100, "status": "Running", "last_error": None})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up orca_bridge from a config entry (UI)."""
    hass.http.register_view(OrcaDevReceiveView())
    _LOGGER.info("orca_bridge integration set up via config entry.")
    hass.data.setdefault(DOMAIN, {"battery": 100, "status": "Running", "last_error": None})
    return True
