# custom_components/orca_bridge/config_flow.py

import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

# Schema used both for initial add and for options
DATA_SCHEMA = vol.Schema({
    vol.Required("dashboard_url", default="http://127.0.0.1:4567/get_dashboard"): str,
    vol.Required("poll_interval", default=5): vol.All(int, vol.Range(min=1)),
    vol.Required("webhook_url", default="http://127.0.0.1:5005/webhooks/rest/webhook"): str,
    vol.Required("sender", default="homeassistant"): str,
})

class OrcaBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial config flow for Orca Bridge."""
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Step shown when user clicks “Add integration”."""
        if user_input is not None:
            # Save the four keys into entry.data
            return self.async_create_entry(title="Orca Bridge", data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

    @staticmethod
    def async_get_options_flow(config_entry):
        """Define the Options flow for reconfiguration."""
        return OrcaBridgeOptionsFlow(config_entry)

class OrcaBridgeOptionsFlow(config_entries.OptionsFlow):
    """Handle options (reconfigure) for Orca Bridge."""
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Show the form to edit the four parameters."""
        if user_input is not None:
            # Save edited values into entry.options
            return self.async_create_entry(title="", data=user_input)

        # Pre-populate with either the original data or last options
        current = {**self.config_entry.data, **self.config_entry.options}

        schema = vol.Schema({
            vol.Required("dashboard_url", default=current["dashboard_url"]): str,
            vol.Required("poll_interval", default=current["poll_interval"]): vol.All(int, vol.Range(min=1)),
            vol.Required("webhook_url", default=current["webhook_url"]): str,
            vol.Required("sender", default=current["sender"]): str,
        })

        return self.async_show_form(step_id="init", data_schema=schema)
