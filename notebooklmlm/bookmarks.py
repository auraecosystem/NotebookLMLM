"""Persistent NoteBookmarks registry with parameterized SQLite storage."""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,127}$")
_PARAM_RE = re.compile(r"(?<!:):([A-Za-z_][A-Za-z0-9_]*)")


@dataclass(frozen=True)
class Bookmark:
    name: str
    query: str
    description: str = ""
    language: str = "sql"
    parameters: dict[str, dict[str, Any]] | None = None
    version: int = 1
    created_at: str = ""
    updated_at: str = ""


def required_parameters(query: str) -> set[str]:
    """Discover named placeholders. For complex SQL, prefer driver validation."""
    return set(_PARAM_RE.findall(query))


class BookmarkRegistry:
    """SQLite-backed registry for reusable query templates."""

    def __init__(self, database: str | Path = "notebooklmlm.db") -> None:
        self._connection = sqlite3.connect(str(database))
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                name TEXT PRIMARY KEY, query TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                language TEXT NOT NULL DEFAULT 'sql',
                parameters_json TEXT NOT NULL DEFAULT '{}',
                version INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            )
        """)
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "BookmarkRegistry":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def add(self, name: str, query: str, description: str = "", language: str = "sql",
            parameters: dict[str, dict[str, Any]] | None = None, replace: bool = False) -> Bookmark:
        if not _NAME_RE.fullmatch(name):
            raise ValueError("Invalid bookmark name")
        if not query.strip():
            raise ValueError("Bookmark query cannot be empty")
        if language not in {"sql", "python", "javascript", "r", "bash", "lmlm"}:
            raise ValueError(f"Unsupported bookmark language: {language}")
        now = datetime.now(timezone.utc).isoformat()
        current = self.get(name, required=False)
        if current and not replace:
            raise ValueError(f"Bookmark already exists: {name}")
        version = current.version + 1 if current else 1
        self._connection.execute("""
            INSERT INTO bookmarks
                (name, query, description, language, parameters_json, version, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                query=excluded.query, description=excluded.description,
                language=excluded.language, parameters_json=excluded.parameters_json,
                version=excluded.version, updated_at=excluded.updated_at
        """, (name, query, description, language, json.dumps(parameters or {}, sort_keys=True),
              version, current.created_at if current else now, now))
        self._connection.commit()
        return self.get(name)

    def get(self, name: str, required: bool = True) -> Bookmark | None:
        row = self._connection.execute("SELECT * FROM bookmarks WHERE name = ?", (name,)).fetchone()
        if row is None:
            if required:
                raise KeyError(f"Bookmark not found: {name}")
            return None
        return Bookmark(
            name=row["name"], query=row["query"], description=row["description"],
            language=row["language"], parameters=json.loads(row["parameters_json"]),
            version=row["version"], created_at=row["created_at"], updated_at=row["updated_at"])

    def list(self) -> list[Bookmark]:
        rows = self._connection.execute("SELECT name FROM bookmarks ORDER BY name").fetchall()
        return [self.get(row["name"]) for row in rows]

    def delete(self, name: str) -> bool:
        cursor = self._connection.execute("DELETE FROM bookmarks WHERE name = ?", (name,))
        self._connection.commit()
        return cursor.rowcount > 0

    def validate_parameters(self, bookmark: Bookmark, values: dict[str, Any]) -> None:
        expected, supplied = required_parameters(bookmark.query), set(values)
        missing, extra = expected - supplied, supplied - expected
        if missing:
            raise ValueError(f"Missing query parameters: {', '.join(sorted(missing))}")
        if extra:
            raise ValueError(f"Unexpected query parameters: {', '.join(sorted(extra))}")
