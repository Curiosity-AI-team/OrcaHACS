from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the dashboard sensor."""
    coord = hass.data[DOMAIN]["coordinator"]
    async_add_entities([OrcaDashboardSensor(coord)], True)

class OrcaDashboardSensor(CoordinatorEntity, Entity):
    """A single sensor that holds your dashboard JSON as attributes."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Orca Dashboard"
        self._attr_unique_id = "orca_bridge_dashboard"

    @property
    def state(self):
        """Use world_name as the sensor’s state."""
        data = self.coordinator.data or {}
        return data.get("world_name", "unknown")

    @property
    def extra_state_attributes(self):
        """Expose the full JSON under attributes."""
        attrs = dict(self.coordinator.data or {})
        # include any replies from the chat service
        last = self.hass.data[DOMAIN].get("last_response")
        if last is not None:
            attrs["last_response"] = last
        return attrs
