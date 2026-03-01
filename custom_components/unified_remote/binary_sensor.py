"""Binary sensor platform for Unified Remote."""
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Unified Remote binary sensor."""
    computers = hass.data[DOMAIN].get("computers", [])
    
    entities = []
    for computer in computers:
        entities.append(UnifiedRemoteStatusSensor(computer))

    async_add_entities(entities, True)

class UnifiedRemoteStatusSensor(BinarySensorEntity):
    """Sensor to track if the Unified Remote server is connected."""

    def __init__(self, computer):
        self._computer = computer
        self._attr_name = f"{computer.name} Connection"
        self._attr_unique_id = f"{computer.host}_connection_status"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return True if connected."""
        return self._computer.is_available

    @property
    def available(self):
        """Always return true so HA doesn't mark the sensor itself as broken."""
        return True
