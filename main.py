from wazuh_sdk.client import WazuhClient, AsyncWazuhClient
from wazuh_sdk.managers.agents import AgentInsertForce
from wazuh_sdk.managers.agents import (
    ListAgentsQueryParams,
    ListAgentsDistinctQueryParams,
    ListOutdatedAgentsQueryParams,
    OsQueryParameters,
    AgentsManager,
)
from wazuh_sdk.managers.syscheck import SysCheckManager

if __name__ == "__main__":
    import asyncio

    client = WazuhClient(
        base_url="https://172.31.255.52:55000",
        username="wazuh",
        password="Qxv93C5MRgS4wea?l2nn+cPWNbs8wN3G",
        version="4",
    )

    async def main():
        async with AsyncWazuhClient(
            base_url="https://172.31.255.52:55000",
            username="wazuh",
            password="Qxv93C5MRgS4wea?l2nn+cPWNbs8wN3G",
            version="4",
        ) as async_client:
            agents_manager = AgentsManager(client=async_client)
            syscheck_manager = SysCheckManager(client=async_client)
            # res = await agents_manager.list()
            # print(res)
            print(await syscheck_manager.get_results(agent_id="001"))

    asyncio.run(main())
