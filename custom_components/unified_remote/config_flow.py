"""Config flow for Unified Remote integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME

from .const import DOMAIN, CONF_RETRY

class UnifiedRemoteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Unified Remote."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Here we could add logic to ping the Unified Remote server to verify it exists
            # For now, we will just create the entry.
            title = user_input.get(CONF_NAME) or user_input.get(CONF_HOST)
            return self.async_create_entry(title=title, data=user_input)

        # The form fields the user will see in the UI
        data_schema = vol.Schema({
            vol.Optional(CONF_NAME, default=""): str,
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=9510): int,
            vol.Optional(CONF_RETRY, default=120): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
