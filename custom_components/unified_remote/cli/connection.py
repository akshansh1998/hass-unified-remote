"""Handle with connection and requests"""
import re
from json import dumps
from uuid import uuid4

import aiohttp

class Connection:
    """Handle with target connection, in this case, with Unified Remote host client."""

    def __init__(self, session: aiohttp.ClientSession):
        self.__url = ""
        self.__source_guid = ""
        self.__headers = {}
        # Uses the persistent http session passed from Home Assistant
        self.__session = session

    async def connect(self, host, port):
        """Establish connection with host client."""
        self.__url = f"http://{host}:{port}/client/"
        assert self.__validate_url(), AssertionError("Malformed URL")
        await self.__set_headers()
        self.__gen_guid()
        await self.__autenticate()

    def __gen_guid(self):
        """Generates an unique id to perform requests."""
        self.__source_guid = f"web-{uuid4()}"

    def __validate_url(self):
        """URL validating."""
        regex = re.compile(
            r"^(?:http|ftp)s?://" 
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|" 
            r"localhost|" 
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" 
            r"(?::\d+)?" 
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, self.__url) is not None

    async def __set_headers(self):
        """Do the first connection to fetch provided Connection ID and set it to request headers."""
        async with self.__session.get(self.__url + "connect") as response:
            data = await response.json()
            conn_id = data["id"]
            self.__headers = {"UR-Connection-ID": conn_id}

    async def __autenticate(self):
        """Do some server authentication to make connection persistent and stable."""
        password = str(uuid4())
        payload = {
            "Action": 0,
            "Request": 0,
            "Version": 10,
            "Password": password,
            "Platform": "web",
            "Source": self.__source_guid,
        }
        async with self.__session.post(
            self.__url + "request", headers=self.__headers, data=dumps(payload)
        ) as resp:
            await resp.text()

        payload = {
            "Capabilities": {
                "Actions": True,
                "Sync": True,
                "Grid": True,
                "Fast": False,
                "Loading": True,
                "Encryption2": True,
            },
            "Action": 1,
            "Request": 1,
            "Source": self.__source_guid,
        }
        async with self.__session.post(
            self.__url + "request", headers=self.__headers, data=dumps(payload)
        ) as resp:
            await resp.text()

    async def exe_remote(self, remoteID, action, extras=None):
        """Executes given remote id and action using a post request."""
        payload = {
            "ID": remoteID,
            "Action": 7,
            "Request": 7,
            "Run": {"Name": action},
            "Source": self.__source_guid,
        }
        if extras is not None:
            payload["Run"]["Extras"] = extras

        async with self.__session.post(
            self.__url + "request", headers=self.__headers, data=dumps(payload)
        ) as response:
            text = await response.text()
            status = response.status
            return {"status_code": status, "content": text.encode("ascii")}

    def get_headers(self):
        return self.__headers

    def get_url(self):
        return self.__url
