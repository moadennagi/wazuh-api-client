from typing import Optional, Any
from dataclasses import dataclass
from ..enums import AgentStatus, GroupConfigStatus
from ..interfaces import AsyncClientInterface
from ..client import AsyncRequestMaker

@dataclass(kw_only=True)
class BaseQueryParameters:
    def to_query_dict(self) -> dict[str, Any]:
        query: dict[str, str] = {}
        for key, value in vars(self).items():
            if value is None:
                continue
            if isinstance(value, list):
                query[key] = ",".join(
                    v.value if hasattr(v, "value") else str(v) for v in value
                )
            elif isinstance(value, bool):
                query[key] = str(value).lower()
            else:
                query[key] = str(value)
        return query

@dataclass(kw_only=True)
class OsQueryParameters(BaseQueryParameters):
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
            if value is None or key == "os_query_parameters":
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

@dataclass
class Error:
    code: int
    message: str
    remediation: str

@dataclass
class FailedItem:
    error: dict[str, dict[str, Error]]
    id: list[str] | list[int]

@dataclass
class OS:
    arch: str
    minor: str
    codename: str
    version: str
    platform: str
    uname: str
    name: str
    major: str

@dataclass
class Agent:
    os: OS
    group_config_status: GroupConfigStatus
    lastKeepAlive: str
    dateAdd: str
    node_name: str
    manager: str
    registerIp: str
    ip: str
    mergedSum: str
    group: list[str]
    configSum: str
    status: AgentStatus
    name: str
    id: str
    version: str
    status_code: int = 0

@dataclass
class ResponseData:
    total_affected_items: int
    failed_items: list[FailedItem]
    total_failed_items: int
    affected_items: list[Agent]

@dataclass
class ListAgentResponse:
    message: str
    error: int
    data: ResponseData


class AgentsManager:
    def __init__(self, client: AsyncClientInterface):
        """
        Initialize with a reference to the WazuhClient instance.
        """
        self.async_request_builder = AsyncRequestMaker(client)

    async def list(self, list_agent_params: Optional[ListAgentsQueryParams] = None) -> ListAgentResponse:
        """
        Retrieve a list of agents.
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agents
        """
        if not list_agent_params:
            list_agent_params = ListAgentsQueryParams()
        res = await self.async_request_builder.get("list_agents", list_agent_params)
        response = ListAgentResponse(**res)
        return response
    
    async def list_distinct(self, list_agents_distinct_params: ListAgentsDistinctQueryParams) -> ListAgentResponse:
        """
        List all the different combinations that agents have for the selected fields.
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_fields
        """
        res = await self.async_request_builder.get("list_agents_distinct", list_agents_distinct_params)
        response = ListAgentResponse(**res)
        return response
    
    async def list_outdated_agents(self, list_outdated_agents: Optional[ListOutdatedAgentsQueryParams] = None) -> ListAgentResponse:
        """
        Return the list of outdated agents.
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_outdated
        """
        if not list_outdated_agents:
            list_outdated_agents = ListOutdatedAgentsQueryParams()
        res = await self.async_request_builder.get("list_outdated_agents", list_outdated_agents)
        response = ListAgentResponse(**res)
        return response
    
    def list_agents_without_group(self):
        pass

    def delete(self):
        pass

    def add(self):
        pass

    def get_active_configuration(self):
        pass

    def remove_agent_from_groups(self):
        pass

    def remove_agent_from_group(self):
        pass

    def assign_agent_to_group(self):
        pass

    def get_key(self):
        pass

    def restart_agent(self):
        pass

    def get_wazuh_daemon_stats(self):
        pass

    def upgrade_agents(self):
        pass

    def upgrade_agents_custom(self):
        pass

    def check_user_permission_to_uninstall_agents(self):
        pass

    def remove_agents_from_group(self):
        pass

    def restart_agents_in_group(self):
        pass

    def add_agent_full(self):
        pass

    def add_agent_quick(self):
        pass


    def restart_agents_in_node(self):
        pass

    def force_reconnect_agents(self):
        pass

    def restart_agents(self):
        pass

    def summarize_agents_os(self):
        pass

    def summarize_agents_status(self):
        pass
    
    def get_upgrade_results(self):
        """
        Return the agents upgrade results
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_upgrade
        """
        pass