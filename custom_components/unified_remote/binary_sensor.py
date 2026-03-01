"""Binary sensor platform for Unified Remote."""
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Unified Remote binary sensor."""
    computers = hass.data[DOMAIN].get("computers", [])
    async_add_entities([UnifiedRemoteStatusSensor(comp) for comp in computers], True)


class UnifiedRemoteStatusSensor(BinarySensorEntity):
    """Sensor to track if the Unified Remote server is connected."""

    def __init__(self, computer):
        self._computer = computer
        self._attr_name = f"{computer.name} Connection"
        self._attr_unique_id = f"{computer.host}_connection_status"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the computer."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._computer.host)},
            name=self._computer.name,
            manufacturer="Unified Remote",
            model="Computer Status",
        )

    @property
    def is_on(self):
        """Return True if connected."""
        return self._computer.is_available

    @property
    def available(self):
        """Always return true so HA doesn't mark the sensor itself as broken."""
        return True
