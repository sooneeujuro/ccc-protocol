"""CCCP local lifecycle supervisor."""

from .models import AdapterResult, EffectClass, RunPolicy, RunState, TaskState
from .store import StateStore
from .supervisor import Supervisor

__all__ = [
    "AdapterResult",
    "EffectClass",
    "RunPolicy",
    "RunState",
    "StateStore",
    "Supervisor",
    "TaskState",
]

__version__ = "0.1.0"
