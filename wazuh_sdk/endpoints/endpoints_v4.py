API_PATHS = {
    "list_agents": "/agents",
    "list_outdated_agents": "/agents/outdated",
    "list_agents_distinct": "/agents/stats/distinct",
    "agent_info": "/agents/{agent_id}",
    "agent_add": "/agents",
    "delete_agents": "/agents",
    "agent_restart": "/agents/{agent_id}/restart",
    "alerts_search": "/syscheck/events",
    "alerts_summary": "/syscheck/summary",
    # Additional endpoints for v4 can be added here.
    "generate_token": "/security/user/authenticate"
}
