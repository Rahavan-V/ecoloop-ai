"""
EcoLoop AI - Abstract Base Agent
Provides foundational lifecycle hooks, execution metrics, and audit logging.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for all EcoLoop autonomous agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.last_execution_ms: float = 0.0

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process input data and return agent findings."""
        pass

    def timed_execution(self, func, *args, **kwargs):
        """Measures agent computation time accurately in milliseconds."""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration_ms = (time.perf_counter() - start) * 1000.0
        self.last_execution_ms = round(duration_ms, 2)
        return result, self.last_execution_ms
