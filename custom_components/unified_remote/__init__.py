"""HA Unified Remote Integration"""
import logging as log
from datetime import timedelta
import aiohttp

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_HOST, CONF_HOSTS, CONF_NAME, CONF_PORT
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.unified_remote.cli.computer import Computer
from custom_components.unified_remote.cli.remotes import Remotes

DOMAIN = "unified_remote"
CONF_RETRY = "retry_delay"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOSTS): vol.Schema(
                    vol.All(
                        [
                            {
                                vol.Optional(CONF_NAME, default=""): cv.string,
                                vol.Required(CONF_HOST, default="localhost"): cv.string,
                                vol.Optional(CONF_PORT, default="9510"): cv.port,
                            }
                        ]
                    )
                ),
                vol.Optional(CONF_RETRY, default=120): int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

DEFAULT_NAME = ""
_LOGGER = log.getLogger(__name__)

COMPUTERS = []
REMOTES = None

def load_remotes(path):
    """Load remotes synchronously (to be run in executor job)."""
    try:
        remotes = Remotes(path)
        _LOGGER.info("Remotes loaded sucessfully")
        return remotes
    except FileNotFoundError:
        _LOGGER.error(f"Remotes file not found. Path:{path}")
    except AssertionError as remote_error:
        _LOGGER.error(str(remote_error))
    except Exception as error:
        _LOGGER.error(str(error))
    return None

async def init_computers(hosts, session):
    for computer in hosts:
        name = computer.get(CONF_NAME)
        host = computer.get(CONF_HOST)
        port = computer.get(CONF_PORT)

        if name == "":
            name = host
        try:
            comp = Computer(name, host, port, session)
            await comp.async_init()
            COMPUTERS.append(comp)
        except (AssertionError, Exception):
            return False
    return True

def find_computer(name):
    for computer in COMPUTERS:
        if computer.name == name:
            return computer
    return None

def validate_response(response):
    """Validate keep alive packet to check if reconnection is needed"""
    out = response["content"].decode("ascii")
    status = response["status_code"]
    flag = 0
    if status != 200:
        _LOGGER.error(f"Keep alive packet was failed. Status code: {status}. Response: {out}")
        flag = 1
    else:
        errors = ["Not a valid connection", "No UR"]
        for error in errors:
            if error in out:
                flag = 1
                break
    if flag == 1:
        raise ConnectionError()

async def async_setup(hass, config):
    """Setting up Unified Remote Integration"""
    global REMOTES
    
    # Resolve dynamic config path instead of hardcoding "/config"
    REMOTE_FILE_PATH = hass.config.path("custom_components/unified_remote/cli/remotes.yml")
    REMOTES = await hass.async_add_executor_job(load_remotes, REMOTE_FILE_PATH)

    hosts = config[DOMAIN].get(CONF_HOSTS)
    retry_delay = config[DOMAIN].get(CONF_RETRY)
    if retry_delay > 120:
        retry_delay = 120

    # Get HA's built in async http client
    session = async_get_clientsession(hass)

    if not await init_computers(hosts, session):
        return False

    async def keep_alive(now):
        """Keep host listening our requests"""
        for computer in COMPUTERS:
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
        if target is None or str(target).strip() == "":
            if not COMPUTERS:
                _LOGGER.error("No computers configured.")
                return
            computer = COMPUTERS[0]
        else:
            computer = find_computer(target)

        if computer is None:
            _LOGGER.error(f"No such computer called {target}")
            return None

        remote_name = call.data.get("remote", DEFAULT_NAME)
        remote_id = call.data.get("remote_id", DEFAULT_NAME)
        action = call.data.get("action", DEFAULT_NAME)
        extras = call.data.get("extras")

        # Allows user to pass remote id without declaring it on remotes.yml
        if remote_id is not None and remote_id != "":
            if action != "":
                await computer.call_remote(remote_id, action, extras)
                return None

        # Check if none or empty service data was parsed.
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

    # Register remote call service asynchronously.
    hass.services.async_register(DOMAIN, "call", handle_call)
    
    # Set interval asynchronously
    async_track_time_interval(hass, keep_alive, timedelta(seconds=retry_delay))

    return True
