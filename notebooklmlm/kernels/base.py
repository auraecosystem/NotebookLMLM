"""Kernel interface."""

from abc import ABC, abstractmethod
from typing import Any

from notebooklmlm.models import ExecutionResult


class Kernel(ABC):
    language: str

    @abstractmethod
    def execute(self, code: str, context: dict[str, Any] | None = None) -> ExecutionResult:
        """Execute source and return a normalized result."""

    def interrupt(self) -> None:
        """Interrupt a running execution when supported."""

    def restart(self) -> None:
        """Reset kernel state when supported."""

    def close(self) -> None:
        """Release kernel resources when supported."""
