"""Switch platform for Unified Remote."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Unified Remote switch platform."""
    computers = hass.data[DOMAIN].get("computers", [])
    async_add_entities([UnifiedRemoteMonitorSwitch(comp) for comp in computers])


class UnifiedRemoteMonitorSwitch(SwitchEntity):
    """Representation of a Unified Remote Monitor Switch."""

    def __init__(self, computer):
        self._computer = computer
        self._attr_unique_id = f"{computer.host}_monitor_switch"
        self._attr_name = f"{computer.name} Monitor"
        self._attr_icon = "mdi:monitor"
        self._is_on = True 

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._computer.host)},
            name=self._computer.name,
            manufacturer="Unified Remote",
            model="Computer Monitor",
        )

    @property
    def is_on(self):
        return self._is_on

    @property
    def available(self):
        return self._computer.is_available

    async def async_turn_on(self, **kwargs):
        await self._computer.call_remote("Unified.Monitor", "turn_on")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._computer.call_remote("Unified.Monitor", "turn_off")
        self._is_on = False
        self.async_write_ha_state()
