from .endpoints.endpoints_v4 import API_PATHS as API_PATHS_V4

def get_api_paths(version: str):
    """
    Return the API endpoints dictionary based on the provided Wazuh version.
    """
    if version.startswith("4"):
        return API_PATHS_V4
    else:
        raise ValueError(f"Unsupported Wazuh version: {version}")
