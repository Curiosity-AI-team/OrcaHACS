import logging
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class OrcaReceiveTextView(HomeAssistantView):
    """POST endpoint to send text to HA Conversation Agent."""
    url = "/api/orca_bridge/receive_text"
    name = "api:orca_bridge:receive_text"
    requires_auth = False

    async def post(self, request):
        hass: HomeAssistant = request.app["hass"]
        try:
            data = await request.json()
            text = data.get("text", "")
            battery = data.get("battery")
            error_code = data.get("error_code")

            if not text:
                return self.json({"error": "Missing 'text' in JSON"}, status=400)

            # store for sensors or UI
            hass.data.setdefault(DOMAIN, {})
            hass.data[DOMAIN]["battery"] = battery
            hass.data[DOMAIN]["last_error"] = error_code

            _LOGGER.info(f"[OrcaBridge] Received text: {text}, Battery: {battery}, Error: {error_code}")

            result = await hass.services.async_call(
                "conversation", "process",
                {"text": text},
                blocking=True,
                return_response=True
            )

            return self.json({
                "status": "ok",
                "input_text": text,
                "conversation_response": result
            })
        except Exception as err:
            _LOGGER.exception("Error in receive_text endpoint")
            return self.json({"error": str(err)}, status=500)
