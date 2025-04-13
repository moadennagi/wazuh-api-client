from typing import Optional, Any, List
from dataclasses import dataclass, field
from ..enums import AgentStatus, GroupConfigStatus, AgentComponent, AgentConfiguration
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
    agents_list: Optional[List[str]] = None
    status: Optional[List[str]] = None
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
    distinct: bool = False  # Look for distinct values.

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
    fields: List[str]


@dataclass(kw_only=True)
class ListOutdatedAgentsQueryParams(CommonListAgentsQueryParams):
    pass


@dataclass(kw_only=True)
class ListAgentsWithoutGroupQueryParams(CommonListAgentsQueryParams):
    pass


@dataclass(kw_only=True)
class DeleteAgentsQueryParams(BaseQueryParameters):
    pretty: Optional[bool] = False
    wait_for_complete: Optional[bool] = False
    older_than: Optional[str] = None
    os_query_parameters: Optional[OsQueryParameters] = None
    q: Optional[str] = None  # Query string (e.g. 'status=active')
    manager: Optional[str] = None
    version: Optional[str] = None
    group: Optional[str] = None
    node_name: Optional[str] = None
    name: Optional[str] = None
    ip: Optional[str] = None
    registerIP: Optional[str] = None
    agents_list: Optional[List[str]] = None
    status: Optional[List[AgentStatus]] = None
    purge: Optional[bool] = False


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
    id: List[str] | List[int]


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
    group: List[str]
    configSum: str
    status: AgentStatus
    name: str
    id: str
    version: str
    status_code: int = 0


@dataclass
class ResponseData:
    total_affected_items: int
    failed_items: List[FailedItem]
    total_failed_items: int
    affected_items: List[Agent]


@dataclass
class ListAgentResponse:
    message: str
    error: int
    data: ResponseData


@dataclass
class AddAgentData:
    id: str
    key: str


@dataclass
class AddAgentResponse:
    data: AddAgentData
    error: int


@dataclass
class Server:
    address: str
    port: int
    max_retries: int
    retry_interval: int
    protocol: str


@dataclass
class Enrollment:
    enabled: str
    delay_after_enrollment: int
    port: int
    ssl_cipher: str
    auto_method: str


@dataclass
class Client:
    config_profile: str = field(metadata={"json": "config-profile"})
    notify_time: int
    time_reconnect: int = field(metadata={"json": "time-reconnect"})
    force_reconnect_interval: int
    ip_update_interval: int
    auto_restart: str
    remote_conf: str
    crypto_method: str
    server: List[Server]
    enrollment: List[Enrollment]


@dataclass
class AgentCofigurationData:
    client: Client


@dataclass
class AgentConfigurationResponse:
    data: AgentCofigurationData
    error: int


class AgentsManager:
    def __init__(self, client: AsyncClientInterface):
        """
        Initialize with a reference to the WazuhClient instance.
        """
        self.async_request_builder = AsyncRequestMaker(client)

    async def list(
        self, list_agent_params: Optional[ListAgentsQueryParams] = None, **kwargs
    ) -> ListAgentResponse:
        """
        Retrieve a list of agents.

        This method accepts either a ListAgentsQueryParams object or individual parameters as keyword arguments.

        Examples:
            # Using a dataclass
            params = ListAgentsQueryParams(status=["active"], limit=100)
            agents = await client.list(params)

            # Using keyword arguments
            agents = await client.list(status=["active"], limit=100)

        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agents
        """
        endpoint = "list_agents"
        if not list_agent_params:
            list_agent_params = ListAgentsQueryParams()

        if kwargs:
            for param, value in kwargs.items():
                if not hasattr(ListAgentsQueryParams, param):
                    raise ValueError(
                        f"Invalid parameter: {param}, keywork argument must be one of : {list(ListAgentsQueryParams.__dataclass_fields__.keys())}"
                    )
                setattr(list_agent_params, param, value)
        params = list_agent_params.to_query_dict()
        res = await self.async_request_builder.get(endpoint, params)
        response = ListAgentResponse(**res)
        return response

    async def list_distinct(
        self,
        fields: Optional[List[str]] = None,
        list_agents_distinct_params: Optional[ListAgentsDistinctQueryParams] = None,
        **kwargs,
    ) -> ListAgentResponse:
        """
        List all the different combinations that agents have for the selected fields.

        This method accepts either a ListAgentsDistinctQueryParams object or individual parameters as keyword arguments.

        One of `fields` or `list_agents_distinct_params` is mandatory, you must provide one. If both are given `fields' takes precedence.

        Examples:
            # Using a dataclass
            params = ListAgentsDistinctQueryParams(fields=["active"], limit=100)
            agents = await client.list(params)

            # Using keyword arguments
            agents = await client.list(fields=["active"], limit=100)

        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_fields
        """
        params = None

        if not list_agents_distinct_params and not fields:
            raise ValueError(
                "At least one parameter should be provided: fields or an instance of ListAgentsDistinctQueryParams"
            )
        elif fields and list_agents_distinct_params:
            # fields takes precedence
            setattr(list_agents_distinct_params, "fields", fields)
        elif fields:
            list_agents_distinct_params = ListAgentsDistinctQueryParams(fields=fields)

        if kwargs:
            for param, value in kwargs.items():
                if not hasattr(ListAgentsDistinctQueryParams, param):
                    raise ValueError(
                        f"Invalid parameter: {param}, keywork argument must be one of : {list(ListAgentsDistinctQueryParams.__dataclass_fields__.keys())}"
                    )
                setattr(list_agents_distinct_params, param, value)

        if list_agents_distinct_params:
            params = list_agents_distinct_params.to_query_dict()
        res = await self.async_request_builder.get("list_agents_distinct", params)
        response = ListAgentResponse(**res)
        return response

    async def list_outdated(
        self,
        list_outdated_agents_params: Optional[ListOutdatedAgentsQueryParams] = None,
        **kwargs,
    ) -> ListAgentResponse:
        """
        Return the list of outdated agents.

        This method accepts either a ListAgentsQueryParams object or individual parameters as keyword arguments.

        Examples:
            # Using a dataclass
            params = ListOutdatedAgentsQueryParams(limit=100)
            agents = await client.list(params)

            # Using keyword arguments
            agents = await client.list(limit=100)

        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_outdated
        """
        params = None
        if not list_outdated_agents_params:
            list_outdated_agents_params = ListOutdatedAgentsQueryParams()

        if kwargs:
            for param, value in kwargs.items():
                if not hasattr(ListAgentsDistinctQueryParams, param):
                    raise ValueError(
                        f"Invalid parameter: {param}, keywork argument must be one of : {list(ListOutdatedAgentsQueryParams.__dataclass_fields__.keys())}"
                    )
                setattr(list_outdated_agents_params, param, value)
        if list_outdated_agents_params:
            params = list_outdated_agents_params.to_query_dict()

        res = await self.async_request_builder.get(
            "list_outdated_agents", params
        )
        response = ListAgentResponse(**res)
        return response

    async def list_without_group(
        self,
        list_agents_without_group_params: Optional[ListAgentsWithoutGroupQueryParams] = None,
        **kwargs,
    ):
        """
        Return a list with all the available agents without an assigned group.

        This method accepts either a ListAgentsWithoutGroupQueryParams object or individual parameters as keyword arguments.

        Examples:
            # Using a dataclass
            params = ListAgentsWithoutGroupQueryParams(limit=100)
            agents = await client.list(params)

            # Using keyword arguments
            agents = await client.list(limit=100)

        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.get_agent_no_group
        """
        params = None
        if not list_agents_without_group_params:
            list_agents_without_group_params = ListAgentsWithoutGroupQueryParams()

        if kwargs:
            for param, value in kwargs.items():
                if not hasattr(ListAgentsDistinctQueryParams, param):
                    raise ValueError(
                        f"Invalid parameter: {param}, keywork argument must be one of : {list(ListAgentsWithoutGroupQueryParams.__dataclass_fields__.keys())}"
                    )
                setattr(list_agents_without_group_params, param, value)
    
        if list_agents_without_group_params:
            params = list_agents_without_group_params.to_query_dict()
        res = await self.async_request_builder.get(
            "list_agents_without_group", params
        )
        response = ListAgentResponse(**res)
        return response

    async def delete(
        self,
        agents_list: List[str],
        status: List[AgentStatus],
        purge: bool = False,
        delete_agents_params: Optional[DeleteAgentsQueryParams] = None,
        **kwargs,
    ):
        """
        Delete all agents or a list of them based on optional criteria
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.delete_agents
        """
        if not delete_agents_params:
            delete_agents_params = DeleteAgentsQueryParams()

        delete_agents_params.agents_list = agents_list
        delete_agents_params.status = status
        delete_agents_params.purge = purge

        if kwargs:
            for param, value in kwargs.items():
                if not hasattr(DeleteAgentsQueryParams, param):
                    raise ValueError(
                        f"Invalid parameter: {param}, keywork argument must be one of : {list(DeleteAgentsQueryParams.__dataclass_fields__.keys())}"
                    )
                setattr(delete_agents_params, param, value)

        res = await self.async_request_builder.delete(
            "delete_agents", delete_agents_params
        )
        response = ListAgentResponse(**res)
        return response

    async def add(
        self,
        name: str,
        ip: str,
        pretty: bool = False,
        wait_for_complete: bool = False,
    ) -> AddAgentResponse:
        """
        Add a new agent.
        """
        add_agent_request_body = AddAgentBodyParams(name=name, ip=ip)
        add_agent_query_params = AddAgentQueryParams(
            pretty=pretty, wait_for_complete=wait_for_complete
        )
        res = await self.async_request_builder.post(
            "add_agent",
            query_params=add_agent_query_params,
            body=add_agent_request_body.to_query_dict(),
        )
        response = AddAgentResponse(**res)
        return response

    async def get_active_configuration(
        self,
        agent_id: str,
        component: AgentComponent,
        configuration: AgentConfiguration,
        pretty: bool = False,
        wait_for_complete: bool = False,
    ) -> AgentConfigurationResponse:
        """
        Return the active configuration the agent is currently using.
        This can be different from the configuration present in the configuration file,
        if it has been modified and the agent has not been restarted yet.
        https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.agent_controller.add_agent
        """
        params: dict[str, bool] = dict(pretty=pretty, wait_for_complete=wait_for_complete)
        path_parameters: dict[str, str | int] = dict(agent_id=str(agent_id), component=str(component), configuration=str(configuration))
        res = await self.async_request_builder.get("get_active_configuration", query_params=params, path_params=path_parameters)
        response = AgentConfigurationResponse(**res)
        return response

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
