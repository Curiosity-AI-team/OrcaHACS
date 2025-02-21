import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_ICON

DOMAIN = "orca_bridge"

DATA_SCHEMA = vol.Schema({
    vol.Optional(CONF_ICON, default="mdi:server"): str,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Orca Bridge."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the user step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=DATA_SCHEMA
            )
        return self.async_create_entry(title="Orca Bridge", data=user_input)
