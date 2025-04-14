from enum import Enum

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
    ASSIGN_AGENT_TO_GROUP = "assign_agent_to_group"
    GET_KEY = "get_key"
    RESTART_AGENT = "restart_agent"
    GET_DAEMON_STATS = "get_daemon_stats"
    GET_AGENT_COMPONENT_STATS = "get_agent_component_stats"
    REMOVE_AGENTS_FROM_GROUP = "remove_agent_from_group"
    ASSIGN_AGENTS_TO_GROUP = "assign_agents_to_group"
    RESTART_AGENTS_IN_GROUP = "restart_agents_in_group"
    ADD_AGENT_FULL = "add_agent_full"
    ADD_AGENT_QUICK = "add_agent_quick"
   
    GENERATE_TOKEN = "/security/user/authenticate"

API_PATHS = {
    V4ApiPaths.LIST_AGENTS.value: "/agents",
    V4ApiPaths.LIST_OUTDATED_AGENTS.value: "/agents/outdated",
    V4ApiPaths.LIST_AGENTS_DISTINCT.value: "/agents/stats/distinct",
    V4ApiPaths.LIST_AGENTS_WITHOUT_GROUP.value: "/agents/no_group",
    V4ApiPaths.DELETE_AGENTS.value: "/agents",
    V4ApiPaths.ADD_AGENT.value: "/agents",
    V4ApiPaths.GET_ACTIVE_CONFIGURATION.value: "/agents/{agent_id}/config/{component}/{configuration}",
    V4ApiPaths.DELETE_AGENT_FROM_GROUPS.value: "/agents/{agent_id}/group",
    V4ApiPaths.DELETE_AGENT_FROM_ONE_GROUP.value: "/agents/{agent_id}/group/{group_id}",
    V4ApiPaths.ASSIGN_AGENT_TO_GROUP.value: "/agents/{group_id}/group/{group_id}",
    V4ApiPaths.GET_KEY.value: "/agents/{agent_id}/key",
    V4ApiPaths.RESTART_AGENT.value: "/agents/{agent_id}/restart",
    V4ApiPaths.GET_DAEMON_STATS.value: "/agents/{agent_id}/daemons/stats",
    V4ApiPaths.GET_AGENT_COMPONENT_STATS.value: "/agents/{agent_id}/stats/{component}",
    V4ApiPaths.REMOVE_AGENTS_FROM_GROUP.value: "/agents/group",
    V4ApiPaths.ASSIGN_AGENT_TO_GROUP.value: "/agents/group",
    V4ApiPaths.RESTART_AGENTS_IN_GROUP.value: "/agents/group/{group_id}/restart",
    V4ApiPaths.ADD_AGENT_FULL.value: "/agents/insert",
    V4ApiPaths.ADD_AGENT_QUICK.value: "/agents/insert/quick",

    
    # Additional endpoints for v4 can be added here.
    "generate_token": "/security/user/authenticate"
}