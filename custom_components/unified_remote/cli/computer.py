import logging as log
import aiohttp

from custom_components.unified_remote.cli.connection import Connection

_LOGGER = log.getLogger(__name__)

class Computer:
    def __init__(self, name: str, host: str, port: int, session: aiohttp.ClientSession):
        self.name = name
        self.host = host
        self.port = port
        self.is_available = False
        self.session = session
        self.connection = Connection(session)

    async def async_init(self):
        """Async initializer to handle the connection."""
        try:
            await self.connect()
        except AssertionError as url_error:
            _LOGGER.error(str(url_error))
            raise
        except aiohttp.ClientError:
            _LOGGER.warning(
                f"At the first moment {self.name} seems down, but the connection will be retried."
            )
        except Exception as e:
            _LOGGER.error(str(e))
            raise

    async def connect(self):
        """Handle with connect function and logs if was successful"""
        await self.connection.connect(self.host, self.port)
        self.is_available = True
        _LOGGER.info(f"Connection to {self.name} established")

    async def reconnect(self):
        self.connection = Connection(self.session)
        await self.connect()

    async def call_remote(self, id, action, extras=None):
        if not self.is_available:
            _LOGGER.error(f"Unable to call remote. {self.name} is unavailable.")
            return None
        try:
            await self.connection.exe_remote(id, action, extras)
            _LOGGER.debug(f'Call -> Remote ID: "{id}"; Action: "{action}"; Extras: "{extras}"')
        except aiohttp.ClientError:
            _LOGGER.error(f"Unable to call remote. {self.name} is unavailable.")

    def set_unavailable(self):
        if self.is_available:
            self.is_available = False
            _LOGGER.info(f"The computer {self.name} is now unavailable")
