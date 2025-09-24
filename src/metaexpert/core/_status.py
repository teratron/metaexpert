from enum import Enum, unique


@unique
class InitStatus(Enum):
    """Initialization status codes."""
    INIT_UNKNOWN = 0
    INIT_SUCCEEDED = 1
    INIT_FAILED = 2
    INIT_PARAMETERS_INCORRECT = 3
    INIT_AGENT_NOT_SUITABLE = 4
