# Wazuh API client

**A flexible Python client for interacting with the Wazuh API.**  
Supports 4 version with modular route handlers and extensive functionality for managing agents, configurations, and more.

## Overview

The Wazuh API client aims to simplify integrations with the Wazuh API by providing well-documented methods and abstractions for each available endpoint.

## Usage

```python
from wazuh_api_client import AsyncWazuhClient
from wazuh_api_client.managers import AgentsManager, SysCheckManager

async with AsyncWazuhClient(
    base_url="https://172.0.0.1:55000",
    username="wazuh",
    password="wazuh",
    version="4",
) as async_client:
    agents_manager = AgentsManager(client=async_client)
    syscheck_manager = SysCheckManager(client=async_client)
    # listing all agents
    agents = await agents_manager.list()
    # getting syschekc resutls
    agent_scan_result = await syscheck_manager.get_results(agent_id="001"))
```
## Installation

### From Source

Clone the repository and install in editable mode:

```bash
git clone https://github.com/moadennagi/wazuh-api-client.git
cd wazuh-api-client
pip install -e .
```

### From Pypi

```bash
pip install wazuh-api-client
```
