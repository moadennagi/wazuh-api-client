from dataclasses import dataclass, field
from ..interfaces import ResourceManagerInterface, AsyncClientInterface
from ..client import AsyncRequestMaker
from ..response import APIResponse, ResponseData
from typing import List
from ..endpoints import V4ApiPaths


@dataclass
class Wazuh:
    wazuh_agentlessd: str = field(metadata={"json_key": "wazuh-agentlessd"})


@dataclass
class ManagerResponseData(ResponseData):
    affected_items: List[Wazuh]


@dataclass
class ManagerApiResponse(APIResponse):
    data: ManagerResponseData


class WazuhManager(ResourceManagerInterface):
    def __init__(self, client: AsyncClientInterface):
        self.async_request_builder = AsyncRequestMaker(client)

    async def get_status(
        self, pretty: bool = False, wait_for_complete: bool = False
    ) -> ManagerApiResponse:
        """
        Return the status of all Wazuh daemons
        """
        params: dict[str, bool] = dict(
            pretty=pretty, wait_for_complete=wait_for_complete
        )
        res = await self.async_request_builder.get(
            V4ApiPaths.GET_WAZUH_STATUS.value, query_params=params
        )
        response = ManagerApiResponse(**res)
        return response

    async def get_information(self):
        pass

    async def get_configuration(self):
        pass

    async def update_wazuh_configuration(self):
        pass

    async def get_wazuh_daemon_stats(self):
        pass

    async def get_stats(self):
        pass

    async def get_stats_hour(self):
        pass

    async def get_stats_week(self):
        pass

    async def get_logs(self):
        pass

    async def get_log_summary(self):
        pass

    async def get_api_config(self):
        pass

    async def restart_manager(self):
        pass

    async def check_config(self):
        pass

    async def get_active_configuration(self):
        pass

    async def check_available_updates(self):
        pass
