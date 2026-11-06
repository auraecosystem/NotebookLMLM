"""SQLite SQL kernel with read-only-by-default connections."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from notebooklmlm.kernels.base import Kernel
from notebooklmlm.models import ExecutionResult


class SQLiteKernel(Kernel):
    language = "sql"

    def __init__(self, database: str | Path, read_only: bool = True, timeout: float = 5.0) -> None:
        self.database, self.read_only, self.timeout = str(database), read_only, timeout
        if read_only:
            uri = Path(self.database).resolve().as_uri() + "?mode=ro"
            self._connection = sqlite3.connect(uri, uri=True, timeout=timeout)
        else:
            self._connection = sqlite3.connect(self.database, timeout=timeout)
        self._connection.row_factory = sqlite3.Row

    def execute(self, code: str, context: dict[str, Any] | None = None) -> ExecutionResult:
        try:
            cursor = self._connection.execute(code, context or {})
            rows = [dict(row) for row in cursor.fetchall()] if cursor.description else []
            columns = [item[0] for item in cursor.description] if cursor.description else []
            if not self.read_only:
                self._connection.commit()
            return ExecutionResult(status="ok", data={
                "columns": columns, "rows": rows, "rowcount": cursor.rowcount})
        except sqlite3.Error as exc:
            if not self.read_only:
                self._connection.rollback()
            return ExecutionResult(status="error", stderr=str(exc))

    def close(self) -> None:
        self._connection.close()
