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
    "assign_group_to_group": "/agents/{group_id}/group/{group_id}",
    "get_key": "/agents/{agent_id}/key",
    "restart_agent": "/agents/{agent_id}/restart",
    "get_daemon_stats": "/agents/{agent_id}/daemons/stats",
    
    "agent_info": "/agents/{agent_id}",
    "agent_restart": "/agents/{agent_id}/restart",
    "alerts_search": "/syscheck/events",
    "alerts_summary": "/syscheck/summary",
    # Additional endpoints for v4 can be added here.
    "generate_token": "/security/user/authenticate"
}

class V4ApiPaths(Enum):
    LIST_AGENTS = "list_agents"
    LIST_OUTDATED_AGENTS = "list_outdated_agents"
    LIST_AGENTS_DISTINCT = "list_agents_distinct"
    LIST_AGENTS_WITHOUT_GROUP = "list_agents_without_group"
    DELETE_AGENTS = "delete_agents"
    ADD_AGENT = "add_agent"
    GET_ACTIVE_CONFIGURATION = "get_active_configuration"
    DELETE_AGENT_FROM_GROUPS =  "delete_agent_from_groups"
    DELETE_AGENT_FROM_ONE_GROUP = "delete_agent_from_one_group"
    ASSIGN_AGENT_TO_GROUP = "assign_group_to_group"
    GET_KEY = "get_key"
    RESTART_AGENT = "restart_agent"
    GET_DAEMON_STATS = "get_daemon_stats"

    AGENT_INFO = "/agents/{agent_id}"
    AGENT_RESTART = "/agents/{agent_id}/restart"
    ALERTS_SEARCH = "/syscheck/events"
    ALERTS_SUMMARY = "/syscheck/summary"
    GENERATE_TOKEN = "/security/user/authenticate"