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