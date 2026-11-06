"""Shared notebook execution facade."""

from __future__ import annotations

from typing import Any

from notebooklmlm.kernels.base import Kernel
from notebooklmlm.models import ExecutionResult
from notebooklmlm.notebook import NotebookCell


class NotebookRuntime:
    def __init__(self) -> None:
        self._kernels: dict[str, Kernel] = {}
        self._execution_count = 0

    def register_kernel(self, kernel: Kernel) -> None:
        if kernel.language in self._kernels:
            raise ValueError(f"Kernel already registered: {kernel.language}")
        self._kernels[kernel.language] = kernel

    def execute(self, language: str, source: str,
                context: dict[str, Any] | None = None) -> ExecutionResult:
        if language not in self._kernels:
            raise KeyError(f"No kernel registered for language: {language}")
        self._execution_count += 1
        result = self._kernels[language].execute(source, context)
        return ExecutionResult(status=result.status, data=result.data, stdout=result.stdout,
                               stderr=result.stderr, execution_count=self._execution_count,
                               metadata=result.metadata)

    def execute_cell(self, cell: NotebookCell) -> ExecutionResult:
        if cell.cell_type == "markdown":
            return ExecutionResult(status="ok", data={"render": "markdown", "source": cell.source})
        return self.execute("python" if cell.cell_type == "code" else "sql", cell.source)

    def close(self) -> None:
        for kernel in self._kernels.values():
            kernel.close()
