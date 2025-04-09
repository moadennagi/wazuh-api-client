from enum import Enum

class AgentStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    NEVER_CONNECTED = "never_connected"
    DISCONNECTED = "disconnected"

class GroupConfigStatus(Enum):
    SYNCED = "synced"
    NOT_SYNCED = "not_synced"
