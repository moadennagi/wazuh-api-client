# Wazuh SDK

**A flexible Python SDK for interacting with the Wazuh API.**  
Supports 4.x version with modular route handlers and extensive functionality for managing agents, configurations, and more.

## Overview

The Wazuh SDK aims to simplify integrations with the Wazuh API by providing well-documented methods and abstractions for each available endpoint. Whether you need to manage agents, retrieve system configurations, or interface with other Wazuh components, this SDK offers a consistent and easy-to-use interface for your Python applications.

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

### TODO

- [] V3 support
- [] Agents routes
    - [x] delete agents
    - [x] list agents
    - [x] add agent
    - [x] get active configuration
    - [x] remove agent from groups
    - [x] remove agent from one group
    - [x] assign agent to group
    - [x] get key
    - [x] restart agent
    - [x] get wazuh daemon stats from an agent
    - [x] get agent's component stats
    - [] upgrade agents
    - [] upgrade agents custom
    - [] get upgrade results
    - [] check user's permission to uninstall agents
    - [x] remove agents from group
    - [x] add agent full
    - [x] add agent quick
    - [x] list agents without group
    - [x] restart agents in node
    - [x] list outdated agents
    - [x] force reconnect agents
    - [x] restart agents in group
    - [x] summarize agents OS
    - [x] summarize agents status
- [] Ciscat
- [] Cluster
- [] Decoders
- [] Events
- [] Experimental
- [] Groups
- [] Lists
- [] Logtest
- [] Manager
- [] Mitre
- [] Overview
- [] Rootcheck
- [] Rules
- [] Sca
- [] Security
- [x] Syscheck
    - [x] run scan
    - [x] get results
    - [x] clear results
    - [x] get last scan datetime
- [] Syscollector
- [] Tasks