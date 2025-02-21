import logging
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)
DOMAIN = "orca_bridge"

class SystemStatusSensor(SensorEntity):
    """Sensor to monitor system status, battery, and errors."""

    def __init__(self, hass, icon):
        self._hass = hass
        self._attr_name = "System Status"
        self._attr_icon = icon
        self._attr_native_value = "Running"

    @property
    def state(self):
        return self._attr_native_value

    async def async_update(self):
        """Update sensor state."""
        self._attr_native_value = (
            "Running" if self._hass.data[DOMAIN]["battery"] > 20 else "Warning"
        )
        _LOGGER.info("System Status Sensor Updated: %s", self._attr_native_value)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor platform from a config entry."""
    icon = entry.data.get("icon", "mdi:server")
    hass.data.setdefault(DOMAIN, {"battery": 100, "status": "Running", "last_error": None})
    async_add_entities([SystemStatusSensor(hass, icon)])
