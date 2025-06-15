# custom_components/orca_bridge/__init__.py

import logging
from datetime import timedelta

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .views import OrcaReceiveTextView

_LOGGER = logging.getLogger(__name__)


async def _fetch_dashboard(hass: HomeAssistant, url: str):
    """Fetch JSON from the external dashboard endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            resp.raise_for_status()
            return await resp.json()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Orca Bridge from a config entry (UI or options)."""
    # Ensure storage dict exists
    hass.data.setdefault(DOMAIN, {})

    # 1) Register the existing HTTP POST view
    hass.http.register_view(OrcaReceiveTextView())

    # 2) Read settings (options override the initial data)
    dashboard_url = entry.options.get("dashboard_url", entry.data["dashboard_url"])
    poll_interval = entry.options.get("poll_interval", entry.data["poll_interval"])
    webhook_url   = entry.options.get("webhook_url",   entry.data["webhook_url"])
    sender_name   = entry.options.get("sender",        entry.data["sender"])

    _LOGGER.debug("Orca Bridge config: dashboard_url=%s poll_interval=%s webhook_url=%s sender=%s",
                  dashboard_url, poll_interval, webhook_url, sender_name)

    # 3) Create a DataUpdateCoordinator to poll the dashboard
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="orca_dashboard",
        update_method=lambda: _fetch_dashboard(hass, dashboard_url),
        update_interval=timedelta(seconds=poll_interval),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN]["coordinator"] = coordinator

    # 4) Forward to the sensor platform (loads sensor.py)
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    # 5) Register a service to send messages to your Rasa webhook
    async def send_message_service(call):
        text = call.data["text"]
        _LOGGER.debug("Orca Bridge send_message called with text=%s", text)

        payload = {"sender": sender_name, "message": text}
        _LOGGER.debug("Orca Bridge POST %s → %s", webhook_url, payload)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                webhook_url,
                json=payload,
            ) as resp:
                _LOGGER.debug("Orca Bridge HTTP status: %s", resp.status)
                resp.raise_for_status()
                data = await resp.json()

        _LOGGER.debug("Orca Bridge response JSON: %s", data)

        # Extract the bot replies
        replies = [msg.get("text", "") for msg in data]
        _LOGGER.debug("Orca Bridge parsed replies: %s", replies)

        hass.data[DOMAIN]["last_response"] = replies

        # Immediately refresh the dashboard sensor so UI updates
        await coordinator.async_request_refresh()


    hass.services.async_register(
        DOMAIN,
        "send_message",
        send_message_service,
        schema=vol.Schema({vol.Required("text"): str}),
    )

    _LOGGER.info(
        "Orca Bridge setup complete: polling %s every %ds, webhook=%s, sender=%s",
        dashboard_url, poll_interval, webhook_url, sender_name
    )
    return True
