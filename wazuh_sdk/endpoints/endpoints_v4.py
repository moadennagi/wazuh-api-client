from enum import Enum


API_PATHS = {
    "list_agents": "/agents",
    "list_outdated_agents": "/agents/outdated",
    "list_agents_distinct": "/agents/stats/distinct",
    "list_agents_without_group": "/agents/no_group",
    "delete_agents": "/agents",
    "add_agent": "/agents",
    "get_active_configuration": "/agents/{agent_id}/config/{component}/{configuration}",
    "delete_agent_from_groups": "/agents/{agent_id}/group",
    "delete_agent_from_one_group": "/agents/{agent_id}/group/{group_id}",
    
    "agent_info": "/agents/{agent_id}",
    "agent_restart": "/agents/{agent_id}/restart",
    "alerts_search": "/syscheck/events",
    "alerts_summary": "/syscheck/summary",
    # Additional endpoints for v4 can be added here.
    "generate_token": "/security/user/authenticate"
}

class V4ApiPaths(Enum):
    LIST_AGENTS = "/agents"
    LIST_OUTDATED_AGENTS = "/agents/outdated"
    LIST_AGENTS_DISTINCT = "/agents/stats/distinct"
    LIST_AGENTS_WITHOUT_GROUP = "/agents/no_group"
    DELETE_AGENTS = "/agents"
    ADD_AGENT = "/agents"
    GET_ACTIVE_CONFIGURATION = "/agents/{agent_id}/config/{component}/{configuration}"
    DELETE_AGENT_FROM_GROUPS = "/agents/{agent_id}/group"
    DELETE_AGENT_FROM_ONE_GROUP = "/agents/{agent_id}/group/{group_id}"
    ASSIGN_AGENT_TO_GROUP = "/agents/{agent_id}/group/{group_id}"

    AGENT_INFO = "/agents/{agent_id}"
    AGENT_RESTART = "/agents/{agent_id}/restart"
    ALERTS_SEARCH = "/syscheck/events"
    ALERTS_SUMMARY = "/syscheck/summary"
    GENERATE_TOKEN = "/security/user/authenticate"