API_PATHS = {
    "list_agents": "/agents",
    "list_outdated_agents": "/agents/outdated",
    "list_agents_distinct": "/agents/stats/distinct",
    "list_agents_without_group": "/agents/no_group",
    "delete_agents": "/agents",
    "add_agent": "/agents",
    "get_active_configuration": "/agents/{agent_id}/config/{component}/{configuration}",
    
    "agent_info": "/agents/{agent_id}",
    "agent_restart": "/agents/{agent_id}/restart",
    "alerts_search": "/syscheck/events",
    "alerts_summary": "/syscheck/summary",
    # Additional endpoints for v4 can be added here.
    "generate_token": "/security/user/authenticate"
}
