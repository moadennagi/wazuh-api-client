from ..resources.query_parameters.agents import CommonAgentQueryParams

class Agents:
    def __init__(self, client):
        """
        Initialize with a reference to the WazuhClient instance.
        """
        self.client = client

    def list(self, params: CommonAgentQueryParams):
        """
        Retrieve a list of agents.
        """
        endpoint = self.client._build_endpoint("agents_list")
        params = params.to_query_dict()
        return self.client._request("GET", endpoint, params=params)

    def get(self, agent_id: str):
        """
        Retrieve information for a specific agent.
        """
        endpoint = self.client._build_endpoint("agent_info", agent_id=agent_id)
        return self.client._request("GET", endpoint)

    def add(self, agent_data: dict):
        """
        Create a new agent.
        """
        endpoint = self.client._build_endpoint("agent_add")
        return self.client._request("POST", endpoint, json=agent_data)

    def delete(self, agent_id: str):
        """
        Delete an agent.
        """
        endpoint = self.client._build_endpoint("agent_delete", agent_id=agent_id)
        return self.client._request("DELETE", endpoint)

    def restart(self, agent_id: str):
        """
        Restart an agent (supported in v4+).
        """
        try:
            endpoint = self.client._build_endpoint("agent_restart", agent_id=agent_id)
        except Exception:
            raise NotImplementedError(
                "Agent restart is not supported for this Wazuh version."
            )
        return self.client._request("POST", endpoint)
