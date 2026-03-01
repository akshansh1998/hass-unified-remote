"""HA Unified Remote Integration"""
import logging as log
from datetime import timedelta
import aiohttp

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_HOSTS, CONF_NAME, CONF_PORT
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.unified_remote.cli.computer import Computer
from custom_components.unified_remote.cli.remotes import Remotes
from .const import DOMAIN, CONF_RETRY

# ... Keep CONFIG_SCHEMA, load_remotes, init_computers, find_computer, and validate_response exactly as they are ...

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Unified Remote component from configuration.yaml."""
    hass.data.setdefault(DOMAIN, {"computers": []})
    
    global REMOTES
    REMOTE_FILE_PATH = hass.config.path("custom_components/unified_remote/cli/remotes.yml")
    REMOTES = await hass.async_add_executor_job(load_remotes, REMOTE_FILE_PATH)

    # Setup YAML configuration if it exists
    if DOMAIN in config:
        hosts = config[DOMAIN].get(CONF_HOSTS, [])
        session = async_get_clientsession(hass)
        await init_computers(hosts, session)
        hass.data[DOMAIN]["computers"].extend(COMPUTERS)

    _register_services(hass)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Unified Remote from a UI config entry."""
    session = async_get_clientsession(hass)
    
    # Adapt UI data to match the format our init function expects
    host_data = [{
        CONF_NAME: entry.data.get(CONF_NAME, ""),
        CONF_HOST: entry.data.get(CONF_HOST),
        CONF_PORT: entry.data.get(CONF_PORT, 9510)
    }]
    
    await init_computers(host_data, session)
    
    # Ensure our global list is updated
    hass.data.setdefault(DOMAIN, {"computers": []})
    for c in COMPUTERS:
        if c not in hass.data[DOMAIN]["computers"]:
            hass.data[DOMAIN]["computers"].append(c)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Logic to disconnect the computer and remove it from the list
    host = entry.data.get(CONF_HOST)
    
    computer_to_remove = None
    for computer in hass.data[DOMAIN]["computers"]:
        if computer.host == host:
            computer_to_remove = computer
            break
            
    if computer_to_remove:
        computer_to_remove.set_unavailable()
        hass.data[DOMAIN]["computers"].remove(computer_to_remove)
        if computer_to_remove in COMPUTERS:
            COMPUTERS.remove(computer_to_remove)

    return True

def _register_services(hass):
    """Register the remote call services."""
    
    async def keep_alive(now):
        """Keep host listening our requests"""
        for computer in hass.data[DOMAIN].get("computers", []):
            try:
                response = await computer.connection.exe_remote("", "")
                _LOGGER.debug("Keep alive packet sent")
                validate_response(response)
            except (ConnectionError, aiohttp.ClientError):
                try:
                    _LOGGER.debug(f"Trying to reconnect with {computer.host}")
                    await computer.reconnect()
                except Exception as error:
                    computer.set_unavailable()
                    _LOGGER.debug(f"Unable to connect with {computer.host}")
                    pass

    async def handle_call(call):
        """Handle the service call."""
        target = call.data.get("target")
        computers_list = hass.data[DOMAIN].get("computers", [])
        
        if target is None or str(target).strip() == "":
            if not computers_list:
                _LOGGER.error("No computers configured.")
                return
            computer = computers_list[0]
        else:
            computer = next((c for c in computers_list if c.name == target), None)

        if computer is None:
            _LOGGER.error(f"No such computer called {target}")
            return None

        remote_name = call.data.get("remote", DEFAULT_NAME)
        remote_id = call.data.get("remote_id", DEFAULT_NAME)
        action = call.data.get("action", DEFAULT_NAME)
        extras = call.data.get("extras")

        if remote_id is not None and remote_id != "":
            if action != "":
                await computer.call_remote(remote_id, action, extras)
                return None

        if remote_name != "" and action != "":
            if REMOTES is None:
                _LOGGER.error("Remotes not initialized properly.")
                return
                
            remote = REMOTES.get_remote(remote_name)
            if remote is None:
                _LOGGER.warning(f"Remote {remote_name} not found. Please check your remotes.yml")
                return None
                
            remote_id = remote["id"]
            if action in remote["controls"]:
                await computer.call_remote(remote_id, action, extras)
            else:
                _LOGGER.warning(f'Action "{action}" doesn\'t exists for remote {remote_name}')

    if not hass.services.has_service(DOMAIN, "call"):
        hass.services.async_register(DOMAIN, "call", handle_call)
        # Using a fixed 120 retry delay for now; can be parameterized later
        async_track_time_interval(hass, keep_alive, timedelta(seconds=120))
