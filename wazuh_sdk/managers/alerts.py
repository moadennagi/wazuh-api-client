class Alerts:
    def __init__(self, client):
        """
        Initialize with a reference to the WazuhClient instance.
        """
        self.client = client

    def list(self):
        """
        Retrieve alerts (endpoint varies by version).
        """
        if self.client.version.startswith("3"):
            endpoint = self.client._build_endpoint("alerts")
        elif self.client.version.startswith("4"):
            endpoint = self.client._build_endpoint("alerts_search")
        else:
            raise NotImplementedError("Alerts are not implemented for this version.")
        return self.client._request("GET", endpoint)

    def summary(self):
        """
        Retrieve an alerts summary (available in Wazuh 4.x).
        """
        if not self.client.version.startswith("4"):
            raise NotImplementedError("Alerts summary is only available in Wazuh 4.x.")
        endpoint = self.client._build_endpoint("alerts_summary")
        return self.client._request("GET", endpoint)
