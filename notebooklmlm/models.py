"""Shared execution result models."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExecutionResult:
    status: str
    data: Any = None
    stdout: str = ""
    stderr: str = ""
    execution_count: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status == "ok"
