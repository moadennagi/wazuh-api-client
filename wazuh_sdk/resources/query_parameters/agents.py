from ...enums import AgentStatus, GroupConfigStatus
from typing import Optional


class BaseQueryParameters:
    def to_query_dict(self) -> dict[str, str]:
        """ """
        query: dict[str, str] = {}

        for key, value in vars(self).items():
            if value is None:
                continue
            query[key] = value
        return query

class OsQueryParameters:
    def __init__(self, platform: str = None, version: str = None, name: str = None):
        self.platform = platform
        self.version = version
        self.name = name

    def to_query_dict(self) -> dict[str, str]:
        """ """
        query = {}
        for key, value in vars(self).items():
            if value:
                query["os"] = {}
                break
        for key, value in vars(self).items():
            if value:
                query["os"][key] = value
        return query


class CommonAgentQueryParams(BaseQueryParameters):
    def __init__(
        self,
        pretty: bool = False,
        wait_for_complete: bool = False,
        agents_list: Optional[list[str]] = None,  # list of Agent IDs as strings
        status: Optional[list[AgentStatus]] = None,
        q: Optional[str] = None,  # Query string (e.g. 'status=active')
        older_than: Optional[str] = None,  # Timeframe string, e.g. '7d'
        os_query_parameters: Optional[OsQueryParameters] = None,
        manager: Optional[str] = None,  # Manager hostname
        version: Optional[str] = None,  # Agent version (e.g. "4.4.0")
        group: Optional[str] = None,  # Agent group (GroupID)
        node_name: Optional[str] = None,  # Node name
        name: Optional[str] = None,  # Agent name
        ip: Optional[
            str
        ] = None,  # IP used by the agent to communicate with the manager
        registerIP: Optional[str] = None,  # IP used when registering the agent
    ):
        self.pretty = pretty
        self.wait_for_complete = wait_for_complete
        self.agents_list = agents_list

        self.status = status
        self.q = q
        self.older_than = older_than
        self.os_query_parameters = os_query_parameters
        self.manager = manager
        self.version = version
        self.group = group
        self.node_name = node_name
        self.name = name
        self.ip = ip
        self.registerIP = registerIP

    def to_query_dict(self) -> dict[str, str]:
        """Converts non-None parameters to a dictionary.
        - For lists, if the element is an AgentStatus, use its value.
        - The os_query_parameters are flattened with the "os." prefix.
        """
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


class ListAgentQueryParams(CommonAgentQueryParams):
    def __init__(
        self,
        offset: int = 0,  # >= 0
        limit: int = 500,  # max 100000, recommended not to exceed 500
        select: Optional[list[str]] = None,  # Array of strings for the fields to return
        sort: Optional[
            str
        ] = None,  # string; use +/- for sorting order and dot notation for nested fields
        search: Optional[str] = None,  # string; prepend "-" for complementary search
        group_config_status: str = GroupConfigStatus.SYNCED.value,  # "synced" or "not synced"
        distinct: bool = False,  # Look for distinct values
    ):
        super().__init__()
        self.offset = offset
        self.limit = limit
        self.select = select
        self.sort = sort
        self.search = search
        self.group_config_status = group_config_status
        self.distinct = distinct


class DeleteAgentsQueryParams(BaseQueryParameters):
    def __init__(
        self,
        agents_list: Optional[list[str]],  # list of Agent IDs as strings
        status: Optional[list[AgentStatus]],
        purge: bool = False,  # Permanently delete an agent from the key store
    ):
        super().__init__(agents_list=agents_list, status=status)
        self.purge = purge


class AddAgentQueryParams(BaseQueryParameters):
    def __init__(self, pretty: bool = False, wait_for_complete: bool = False):
        self.pretty = pretty
        self.wait_for_complete = False


class AddAgentBodyParams(BaseQueryParameters):
    def __init__(self, name: str, ip: str = None):
        self.name = name
        self.ip = ip