# custom_components/orca_bridge/__init__.py

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)
DOMAIN = "orca_bridge"

# existing endpoints...

class OrcaReceiveTextView(HomeAssistantView):
    url = "/api/orca_bridge/receive_text"
    name = "api:orca_bridge:receive_text"
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()
        text = data.get("text")
        battery = data.get("battery")
        error_code = data.get("error_code")

        if text is None:
            return self.json({"error": "Missing 'text'"}, status=400)

        hass.data[DOMAIN]["battery"] = battery
        hass.data[DOMAIN]["last_error"] = error_code

        _LOGGER.info(f"[OrcaBridge] text='{text}', battery={battery}, error={error_code}")

        # send to HA conversation agent
        await hass.services.async_call(
            "conversation", "process", {"text": text}, blocking=False
        )
        return self.json({"status": "ok", "text": text})


class OrcaDevicesView(HomeAssistantView):
    url = "/api/orca_bridge/devices"
    name = "api:orca_bridge:devices"
    requires_auth = False

    async def get(self, request):
        # your existing devices logic…
        return self.json({"devices": []})


# ─── NEW ───────────────────────────────────────────────────────────────────────

class OrcaStatusView(HomeAssistantView):
    """GET the entire orca_bridge status dict."""
    url = "/api/orca_bridge/orcava_status"
    name = "api:orca_bridge:orcava_status"
    requires_auth = False

    async def get(self, request):
        hass = request.app["hass"]
        try:
            status = hass.data.get(DOMAIN, {})
            return self.json({"status": status})
        except Exception as e:
            _LOGGER.exception("Error in orcava_status")
            return self.json({"error": str(e)}, status=500)


class OrcaPushView(HomeAssistantView):
    """POST a command into orca_bridge."""
    url = "/api/orca_bridge/orcava_push"
    name = "api:orca_bridge:orcava_push"
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        try:
            data = await request.json()
            command = data.get("command")
            if not command:
                return self.json({"error": "Missing 'command'"}, status=400)

            hass.data[DOMAIN]["last_command"] = command
            _LOGGER.info(f"[OrcaBridge] pushed command: {command}")

            # …you could raise an event or call a service here…

            return self.json({"status": "ok", "received": command})
        except Exception as e:
            _LOGGER.exception("Error in orcava_push")
            return self.json({"error": str(e)}, status=500)


# ─── setup ────────────────────────────────────────────────────────────────────

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.http.register_view(OrcaReceiveTextView())
    hass.http.register_view(OrcaDevicesView())
    hass.http.register_view(OrcaStatusView())
    hass.http.register_view(OrcaPushView())

    hass.data.setdefault(DOMAIN, {
        "battery": 100,
        "last_error": None,
        "status": "Running",
        "last_command": None,
    })
    _LOGGER.info("orca_bridge (YAML) setup completed.")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.http.register_view(OrcaReceiveTextView())
    hass.http.register_view(OrcaDevicesView())
    hass.http.register_view(OrcaStatusView())
    hass.http.register_view(OrcaPushView())

    hass.data.setdefault(DOMAIN, {
        "battery": 100,
        "last_error": None,
        "status": "Running",
        "last_command": None,
    })
    _LOGGER.info("orca_bridge (UI) setup completed.")
    return True
