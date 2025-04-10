import requests

from ssl import SSLContext
from httpx import AsyncClient, RequestError
from typing import Optional

from .constants import DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import WazuhError, WazuhConnectionError
from .utils import get_api_paths

from .interfaces import ClientInterface, AsyncClientInterface


class WazuhClient(ClientInterface):
    
    def __init__(self, base_url: str, version: str, username: str, password: str, verify: bool | None = False):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update({"User-Agent": USER_AGENT})

        # Detect or set the Wazuh version.
        self.version = version or self._detect_version()

        token = self._generate_token(username, password)
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        
        try:
            self.api_paths = get_api_paths(self.version)
        except ValueError as ve:
            raise WazuhError(str(ve))
    
    def _generate_token(self, username: str, password: str) -> str:
        """
        """
        generate_token_url = self.build_endpoint("generate_token")
        response = self.session.post(generate_token_url, verify=False, auth=(username, password))
        response.raise_for_status()
        token = response.json()["data"]["token"]
        return token
    
    def _detect_version(self) -> str:
        """
        Auto-detect the Wazuh version by calling an endpoint. 
        Assumes that '/manager/info' returns JSON with a 'data' dict containing a 'version' field.
        """
        try:
            response = self.session.get(f"{self.base_url}/manager/info", timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            info = response.json()
            version = info.get("data", {}).get("version")
            if not version:
                raise WazuhError("Wazuh version information not found in manager info response.")
            return version
        except Exception as e:
            raise WazuhConnectionError("Failed to detect Wazuh version.") from e
    
    def build_endpoint(self, key: str) -> str:
        """
        Construct the full API endpoint URL using the mapping and provided parameters.
        """
        routes = get_api_paths(self.version)
        route_template = routes[key]
        if not route_template:
            raise WazuhError(f"Endpoint for key '{key}' not found in API mapping for version {self.version}.")
        return self.base_url + route_template.format(key)
    
    def request(self, method: str, endpoint: str, **kwargs):
        """
        Helper method to make an HTTP request.
        """
        try:
            response = self.session.request(method, endpoint, timeout=DEFAULT_TIMEOUT, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise WazuhConnectionError("HTTP request failed.") from e


class AsyncWazuhClient(AsyncClientInterface):
    def __init__(self, base_url: str, version: str, username: str, password: str, verify: SSLContext | str | bool = False):
        self.base_url = base_url.rstrip("/")
        self.verify = verify
        self.username = username
        self.password = password
        self.version = version
        self.client = AsyncClient(
            base_url=self.base_url,
            headers={"User-Agent": USER_AGENT},
            verify=verify,
            timeout=DEFAULT_TIMEOUT
        )
        self.authenticated = False

    async def async_init(self):
        token = await self._generate_token(self.username, self.password)
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        try:
            self.api_paths = get_api_paths(self.version)
        except ValueError as ve:
            raise WazuhError(str(ve))
        self.authenticated = True

    async def _generate_token(self, username: str, password: str) -> str:
        url = self.build_endpoint("generate_token")
        response = await self.client.post(url, auth=(username, password))
        response.raise_for_status()
        return response.json()["data"]["token"]

    async def _detect_version(self) -> str:
        try:
            response = await self.client.get("/manager/info")
            response.raise_for_status()
            version = response.json().get("data", {}).get("version")
            if not version:
                raise WazuhError("Wazuh version not found in manager info response.")
            return version
        except Exception as e:
            raise WazuhConnectionError("Failed to detect Wazuh version.") from e

    def build_endpoint(self, key: str) -> str:
        """
        Construct the full API endpoint URL using the mapping and provided parameters.
        """
        routes = get_api_paths(self.version)
        route_template = routes[key]
        if not route_template:
            raise WazuhError(f"Endpoint for key '{key}' not found in API mapping for version {self.version}.")
        return self.base_url + route_template.format(key)

    async def request(self, method: str, endpoint: str, **kwargs):
        if not self.authenticated:
            await self.async_init()
        
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestError as e:
            raise WazuhConnectionError("HTTP request failed.") from e
        finally:
            await self.close()

    async def close(self):
        if self.client:
            await self.client.aclose()

    async def __aenter__(self):
        await self.async_init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __del__(self):
        # Warn if client wasn't closed explicitly.
        if self.client and not self.client.is_closed:
            import warnings
            warnings.warn("AsyncWazuhClient was not closed explicitly. Use 'async with' or call 'await client.close()'.")
