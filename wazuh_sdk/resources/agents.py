from typing import Optional
from dataclasses import dataclass
from ..enums import AgentStatus, GroupConfigStatus
from ..interfaces import ClientInterface


@dataclass(kw_only=True)
class OsQueryParameters:
    platform: Optional[str] = None
    version: Optional[str] = None
    name: Optional[str] = None

    def to_query_dict(self) -> dict[str, dict[str, str]]:
        """ """
        query: dict[str, dict[str, str]] = {"os": {}}
        for key, value in vars(self).items():
            if value:
                query["os"][key] = value
        return query


@dataclass(kw_only=True)
class BaseQueryParameters:
    def to_query_dict(self) -> dict[str, str]:
        """ """
        query: dict[str, str] = {}
        for key, value in vars(self).items():
            if value is None:
                continue
            query[key] = value
        return query


@dataclass(kw_only=True)
class CommonListAgentsQueryParams(BaseQueryParameters):
    pretty: Optional[bool] = False
    wait_for_complete: Optional[bool] = False
    offset: Optional[int] = 0
    limit: Optional[int] = 500  # max 100000, recommended not to exceed 500
    sort: Optional[str] = (
        None  # string; use +/- for sorting order and dot notation for nested fields
    )
    search: Optional[str] = None  # string; prepend "-" for complementary search
    select: Optional[list[str]] = None
    q: Optional[str] = None  # Query string (e.g. 'status=active')

    def __post_init__(self):
        # Validation logic
        if self.offset < 0:
            raise ValueError("offset must be >= 0")
        if not (0 < self.limit <= 100000):
            raise ValueError("limit must be > 0 and <= 100000")


@dataclass(kw_only=True)
class ListAgentsQueryParams(CommonListAgentsQueryParams):
    agents_list: Optional[list[str]] = None
    status: Optional[list[str]] = None
    older_than: Optional[str] = None
    os_query_parameters: Optional[OsQueryParameters] = None
    manager: Optional[str] = None
    version: Optional[str] = None
    group: Optional[str] = None
    node_name: Optional[str] = None
    name: Optional[str] = None
    ip: Optional[str] = None
    registerIP: Optional[str] = None
    group_config_status: Optional[GroupConfigStatus] = GroupConfigStatus.SYNCED
    distinct: bool = False # Look for distinct values.

    def to_query_dict(self) -> dict[str, str]:
        """Converts non-None parameters to a dictionary."""
        query: dict[str, str] = {}

        for key, value in vars(self).items():
            if value is None:
                continue

            if key == "select" and isinstance(value, list):
                query[key] = ",".join(value)
            elif key == "agents_list" and isinstance(value, list):
                query[key] = ",".join(value)
            elif key == "status" and isinstance(value, list):
                # Convert each AgentStatus enum to its value.
                query[key] = ",".join(
                    elem.value if isinstance(elem, AgentStatus) else str(elem)
                    for elem in value
                )
            elif isinstance(value, bool):
                query[key] = str(value).lower()
            else:
                query[key] = str(value)

        if self.os_query_parameters:
            os_dict = self.os_query_parameters.to_query_dict()
            for os_key, os_val in os_dict.get("os", {}).items():
                query[f"os.{os_key}"] = os_val

        return query
  

@dataclass(kw_only=True)
class ListAgentsDistinctQueryParams(CommonListAgentsQueryParams):
    fields: list[str]

@dataclass(kw_only=True)
class ListOutdatedAgentsQueryParams(CommonListAgentsQueryParams):
    pass

@dataclass(kw_only=True)
class DeleteAgentsQueryParams(BaseQueryParameters):
    status: Optional[list[AgentStatus]]
    agents_list: Optional[list[str]] = None  # list of Agent IDs as strings
    purge: bool = False  # Permanently delete an agent from the key store


@dataclass(kw_only=True)
class AddAgentQueryParams(BaseQueryParameters):
    pretty: Optional[bool] = False
    wait_for_complete: Optional[bool] = False


@dataclass(kw_only=True)
class AddAgentBodyParams(BaseQueryParameters):
    name: str
    ip: Optional[str] = None


class Agents:
    def __init__(self, client: ClientInterface):
        """
        Initialize with a reference to the WazuhClient instance.
        """
        self.client = client

    def list(self, list_agent_params: Optional[ListAgentsQueryParams] = None):
        """
        Retrieve a list of agents.
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agents
        """
        if not list_agent_params:
            list_agent_params = ListAgentsQueryParams()
        endpoint = self.client.build_endpoint("list_agent")
        return self.client.request(
            "GET", endpoint, params=list_agent_params.to_query_dict()
        )
    
    def list_distinct(self, list_agents_distinct_params: ListAgentsDistinctQueryParams):
        """
        List all the different combinations that agents have for the selected fields
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_fields
        """
        endpoint = self.client.build_endpoint("list_agents_distinct")
        return self.client.request(
            "GET", endpoint, params=list_agents_distinct_params.to_query_dict()
        )
    
    def list_outdated_agents(self, list_outdated_agents: Optional[ListOutdatedAgentsQueryParams] = None):
        """
        Return the list of outdated agents
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_outdated
        """
        if not list_outdated_agents:
            list_outdated_agents = ListOutdatedAgentsQueryParams()
        endpoint = self.client.build_endpoint("list_outdated_agents")
        return self.client.request(
            "GET", endpoint, params=list_outdated_agents.to_query_dict()
        )
    
    def get_upgrade_results(self):
        """
        Return the agents upgrade results
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_upgrade
        """
        pass


    def delete(self):
        """
        Delete an agent.
        """
        endpoint = self.client.build_endpoint("agent_delete")
        return self.client.request("DELETE", endpoint)
