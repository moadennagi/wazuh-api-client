from wazuh_api_client.client import AsyncWazuhClient
import asyncio
from wazuh_api_client.managers import AgentsManager

if __name__ == "__main__":

    async def main():
        async with AsyncWazuhClient(
            base_url="https://172.31.255.52:55000/", version="4", username="wazuh", password="Qxv93C5MRgS4wea?l2nn+cPWNbs8wN3G"
        ) as client:
            agents_manager = AgentsManager(client=client)
            print(await agents_manager.list())

    asyncio.run(main())
