import requests
from typing import Optional

from .constants import DEFAULT_TIMEOUT, USER_AGENT
from .exceptions import WazuhError, WazuhConnectionError
from .utils import get_api_paths
from .interfaces import ClientInterface

# Import resource classes
from .resources.agents import Agents
from .resources.alerts import Alerts

class WazuhClient(ClientInterface):
    def __init__(self, base_url: str, version: str, username: str, password: str, verify: Optional[bool] = False):
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
        
        
        # Initialize resources, passing the client instance.
        self.agents = Agents(self)
        self.alerts = Alerts(self)
    
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
