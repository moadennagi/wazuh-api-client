# Wazuh API client

**A flexible Python client for interacting with the Wazuh API.**  
Supports 4.x version with modular route handlers and extensive functionality for managing agents, configurations, and more.

## Overview

The Wazuh API client aims to simplify integrations with the Wazuh API by providing well-documented methods and abstractions for each available endpoint. Whether you need to manage agents, retrieve system configurations, or interface with other Wazuh components, this SDK offers a consistent and easy-to-use interface for your Python applications.

## Usage

```python
from wazuh_sdk import AsyncWazuhClient
from wazuh_sdk.managers import AgentsManager, SysCheckManager

async with AsyncWazuhClient(
    base_url="https://172.0.0.1:55000",
    username="wazuh",
    password="wazuh",
    version="4",
) as async_client:
    agents_manager = AgentsManager(client=async_client)
    syscheck_manager = SysCheckManager(client=async_client)
    # res = await agents_manager.list()
    # print(res)
    print(await syscheck_manager.get_results(agent_id="001"))
    print(await syscheck_manager.clear_results(agent_id="001"))
    print(await syscheck_manager.get_last_scan_datetime(agent_id="001"))

```
## Installation

### From Source

Clone the repository and install in editable mode:

```bash
git clone https://github.com/moadennagi/wazuh-api-sdk.git
cd wazuh-api-sdk
pip install -e .
```
