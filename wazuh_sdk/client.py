import requests
import dataclasses

from ssl import SSLContext
from httpx import AsyncClient, RequestError
from typing import Any, Optional

from .constants import DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import WazuhError, WazuhConnectionError
from .utils import get_api_paths

from .interfaces import (
    ClientInterface,
    AsyncClientInterface,
    AsyncRequestBuilderInterface,
    RequestBuilderInterface,
)


class WazuhClient(ClientInterface):
    def __init__(
        self,
        base_url: str,
        version: str,
        username: str,
        password: str,
        verify: bool | None = False,
    ):
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
        """ """
        generate_token_url = self.build_endpoint("generate_token")
        response = self.session.post(
            generate_token_url, verify=False, auth=(username, password)
        )
        response.raise_for_status()
        token = response.json()["data"]["token"]
        return token

    def _detect_version(self) -> str:
        """
        Auto-detect the Wazuh version by calling an endpoint.
        Assumes that '/manager/info' returns JSON with a 'data' dict containing a 'version' field.
        """
        try:
            response = self.session.get(
                f"{self.base_url}/manager/info", timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            info = response.json()
            version = info.get("data", {}).get("version")
            if not version:
                raise WazuhError(
                    "Wazuh version information not found in manager info response."
                )
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
            raise WazuhError(
                f"Endpoint for key '{key}' not found in API mapping for version {self.version}."
            )
        return self.base_url + route_template.format(key)

    def request(self, method: str, endpoint: str, **kwargs):
        """
        Helper method to make an HTTP request.
        """
        try:
            response = self.session.request(
                method, endpoint, timeout=DEFAULT_TIMEOUT, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise WazuhConnectionError("HTTP request failed.") from e


class AsyncWazuhClient(AsyncClientInterface):
    def __init__(
        self,
        base_url: str,
        version: str,
        username: str,
        password: str,
        verify: SSLContext | str | bool = False,
    ):
        self.base_url = base_url.rstrip("/")
        self.verify = verify
        self.username = username
        self.password = password
        self.version = version
        self.client: Optional[AsyncClient] = None
        self.authenticated = False
        self.api_paths: dict[str, str] = {}

    async def async_init(self):
        self.client = AsyncClient(
            base_url=self.base_url,
            headers={"User-Agent": USER_AGENT},
            verify=self.verify,
            timeout=DEFAULT_TIMEOUT,
        )
        # Optionally detect version if not provided.
        if not self.version:
            self.version = await self._detect_version()
        # Generate token and update headers.
        token = await self._generate_token(self.username, self.password)
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        try:
            self.api_paths = get_api_paths(self.version)
        except ValueError as ve:
            raise WazuhError(str(ve))

        self.authenticated = True

    async def _generate_token(self, username: str, password: str) -> str:
        if self.client is None:
            raise RuntimeError("Async client is not initialized")

        url = self.build_endpoint("generate_token")
        response = await self.client.post(url, auth=(username, password))
        response.raise_for_status()
        return response.json()["data"]["token"]

    async def _detect_version(self) -> str:
        if self.client is None:
            raise RuntimeError("Async client is not initialized")

        try:
            response = await self.client.get("/manager/info")
            response.raise_for_status()
            version = response.json().get("data", {}).get("version")
            if not version:
                raise WazuhError("Wazuh version not found in manager info response.")
            return version
        except Exception as e:
            raise WazuhConnectionError("Failed to detect Wazuh version.") from e

    def build_endpoint(
        self, key: str, params: Optional[dict[str, str | int]] = None
    ) -> str:
        """
        Construct the full API endpoint URL using the mapping and provided parameters.
        """
        routes = get_api_paths(self.version)
        route_template = routes[key]
        if not route_template:
            raise WazuhError(
                f"Endpoint for key '{key}' not found in API mapping for version {self.version}."
            )
        res = self.base_url
        if params:
            for k, v in params.items():
                if not v:
                    del params[k]
            res += route_template.format(**params)
        else:
            res += route_template
        return res

    async def request(self, method: str, endpoint: str, **kwargs):
        if self.client is None:
            raise RuntimeError("Async client is not initialized")

        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestError as e:
            raise Exception("HTTP request failed.") from e

    async def close(self):
        if self.client:
            await self.client.aclose()

    async def __aenter__(self):
        await self.async_init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class AsyncRequestMaker(AsyncRequestBuilderInterface):
    def __init__(self, client: AsyncClientInterface):
        self.client = client

    async def get(
        self,
        endpoint_name: str,
        query_params: Optional[dict] = None,
        path_params: Optional[dict[str, str | int]] = None,
    ) -> Any:
        endpoint = self.client.build_endpoint(endpoint_name, path_params)
        res = await self.client.request("GET", endpoint, params=query_params)
        return res

    async def delete(
        self,
        endpoint_name: str,
        query_params: Any,
        path_params: Optional[dict[str, str | int]] = None,
    ) -> Any:
        endpoint = self.client.build_endpoint(endpoint_name, path_params)
        res = await self.client.request("DELETE", endpoint, params=query_params)
        return res

    async def post(
        self,
        endpoint_name: str,
        query_params: Any,
        body: dict[str, Any],
        path_params: Optional[dict[str, str | int]] = None,
    ) -> Any:
        endpoint = self.client.build_endpoint(endpoint_name, path_params)
        res = await self.client.request(
            "POST", endpoint, params=query_params, json=body
        )
        return res

    async def put(
        self,
        endpoint_name: str,
        query_params: Any,
        path_params: dict[str, str | int],
        body: Optional[dict[str, Any]] = None,
    ) -> Any:
        endpoint = self.client.build_endpoint(endpoint_name, path_params)
        res = await self.client.request("PUT", endpoint, params=query_params, json=body)
        return res


class RequestMaker(RequestBuilderInterface):
    def __init__(self, client: ClientInterface):
        self.client = client

    def get(self, endpoint_name: str, query_params: Any) -> Any:
        endpoint = self.client.build_endpoint(endpoint_name)
        params = query_params.to_query_dict()
        return self.client.request("GET", endpoint, params=params)
