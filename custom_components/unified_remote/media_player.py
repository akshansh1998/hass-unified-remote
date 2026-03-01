"""Media player platform for Unified Remote."""
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_ON, STATE_IDLE
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

# Removed the invalid PLAY_PAUSE flag from this list
SUPPORTED_FEATURES = (
    MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.NEXT_TRACK
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_MUTE
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Unified Remote media player."""
    computers = hass.data[DOMAIN].get("computers", [])
    async_add_entities([UnifiedRemoteMediaPlayer(comp) for comp in computers])


class UnifiedRemoteMediaPlayer(MediaPlayerEntity):
    """Media Player for Unified Remote."""

    def __init__(self, computer):
        self._computer = computer
        self._attr_name = f"{computer.name} Media Controls"
        self._attr_unique_id = f"{computer.host}_media_player"
        self._attr_supported_features = SUPPORTED_FEATURES
        self._attr_icon = "mdi:speaker-multiple"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._computer.host)},
            name=self._computer.name,
            manufacturer="Unified Remote",
            model="Computer Media",
        )

    @property
    def state(self):
        """Return the state of the device."""
        return STATE_ON if self._computer.is_available else STATE_IDLE

    @property
    def available(self):
        return self._computer.is_available

    async def async_media_play_pause(self):
        await self._computer.call_remote("Unified.Media", "play_pause")

    async def async_media_play(self):
        await self._computer.call_remote("Unified.Media", "play_pause")

    async def async_media_pause(self):
        await self._computer.call_remote("Unified.Media", "play_pause")

    async def async_media_next_track(self):
        await self._computer.call_remote("Unified.Media", "next")

    async def async_media_previous_track(self):
        await self._computer.call_remote("Unified.Media", "previous")

    async def async_volume_up(self):
        await self._computer.call_remote("Unified.Media", "volume_up")

    async def async_volume_down(self):
        await self._computer.call_remote("Unified.Media", "volume_down")

    async def async_mute_volume(self, mute):
        await self._computer.call_remote("Unified.Media", "volume_mute")
