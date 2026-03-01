"""Button platform for Unified Remote."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

POWER_ACTIONS = {
    "shutdown": {"name": "Shutdown", "icon": "mdi:power"},
    "restart": {"name": "Restart", "icon": "mdi:restart"},
    "sleep": {"name": "Sleep", "icon": "mdi:sleep"},
    "hibernate": {"name": "Hibernate", "icon": "mdi:power-sleep"},
    "lock": {"name": "Lock", "icon": "mdi:lock"},
    "logoff": {"name": "Logoff", "icon": "mdi:logout"},
    "abort": {"name": "Abort Power Action", "icon": "mdi:close-circle-outline"},
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Unified Remote buttons."""
    computers = hass.data[DOMAIN].get("computers", [])
    entities = []
    for comp in computers:
        for action_id, config in POWER_ACTIONS.items():
            entities.append(UnifiedRemotePowerButton(comp, action_id, config))
    async_add_entities(entities)


class UnifiedRemotePowerButton(ButtonEntity):
    """Representation of a Unified Remote Power Button."""

    def __init__(self, computer, action_id, config):
        self._computer = computer
        self._action_id = action_id
        self._attr_name = f"{computer.name} {config['name']}"
        self._attr_unique_id = f"{computer.host}_power_{action_id}"
        self._attr_icon = config["icon"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._computer.host)},
            name=self._computer.name,
            manufacturer="Unified Remote",
            model="Computer Controls",
        )

    @property
    def available(self):
        """Return True if the computer is connected."""
        return self._computer.is_available

    async def async_press(self) -> None:
        """Handle the button press."""
        # Using the "Unified.Power" ID as defined in remotes.yml
        await self._computer.call_remote("Unified.Power", self._action_id)
