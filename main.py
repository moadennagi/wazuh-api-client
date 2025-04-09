from wazuh_sdk.client import WazuhClient
from wazuh_sdk.resources.query_parameters.agents import ListAgentQueryParams

if __name__ == "__main__":
    client = WazuhClient(
        base_url="https://172.31.255.52:55000", username="wazuh", password="Qxv93C5MRgS4wea?l2nn+cPWNbs8wN3G", version="4"
    )
    parameters = ListAgentQueryParams()
    agents = client.agents.list(params=parameters)
    print(agents)