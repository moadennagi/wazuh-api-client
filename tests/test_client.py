import unittest
from unittest.mock import patch, Mock
from wazuh_sdk.client import WazuhClient
from wazuh_sdk.exceptions import WazuhError

class TestWazuhClient(unittest.TestCase):
    @patch('wazuh_sdk.client.requests.Session.get')
    def test_detect_version(self, mock_get):
        # Simulate a response from /manager/info
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"version": "4.2.1"}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = WazuhClient("http://localhost:55000")
        self.assertEqual(client.version, "4.2.1")
    
    @patch('wazuh_sdk.client.requests.Session.request')
    @patch('wazuh_sdk.client.WazuhClient._detect_version', return_value="4.2.1")
    def test_get_agent_info(self, mock_detect_version, mock_request):
        # Simulate agent info response
        fake_response = {"data": {"id": "001", "name": "Agent001"}}
        mock_request.return_value = fake_response
        
        client = WazuhClient("http://localhost:55000", version="4.2.1")
        result = client.agents.get("001")
        self.assertEqual(result["data"]["name"], "Agent001")
    
    def test_build_endpoint_failure(self):
        client = WazuhClient("http://localhost:55000", version="4.2.1")
        with self.assertRaises(Exception):
            # Attempting to get an endpoint that doesn't exist should raise an error.
            client._build_endpoint("non_existing_key", agent_id="001")

if __name__ == '__main__':
    unittest.main()
