from enum import Enum

class AgentStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    NEVER_CONNECTED = "never_connected"
    DISCONNECTED = "disconnected"

    def __str__(self):
        return self.value

class GroupConfigStatus(Enum):
    SYNCED = "synced"
    NOT_SYNCED = "not_synced"

    def __str__(self):
        return self.value