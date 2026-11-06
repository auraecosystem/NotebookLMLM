"""Versioned notebook document model and JSON serialization."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

CellType = Literal["markdown", "code", "sql"]


@dataclass
class NotebookCell:
    cell_type: CellType
    source: str
    id: str = field(default_factory=lambda: str(uuid4()))
    outputs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    execution_count: int | None = None


@dataclass
class NotebookDocument:
    cells: list[NotebookCell] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    format_name: str = "notebooklmlm"
    format_version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add_cell(self, cell_type: CellType, source: str) -> NotebookCell:
        if cell_type not in ("markdown", "code", "sql"):
            raise ValueError(f"Unsupported cell type: {cell_type}")
        cell = NotebookCell(cell_type=cell_type, source=source)
        self.cells.append(cell)
        return cell

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "NotebookDocument":
        if payload.get("format_name") != "notebooklmlm":
            raise ValueError("Not a NotebookLMLM document")
        version = payload.get("format_version")
        if version != 1:
            raise ValueError(f"Unsupported notebook format version: {version}")
        cells = [NotebookCell(**item) for item in payload.get("cells", [])]
        return cls(
            cells=cells,
            metadata=payload.get("metadata", {}),
            format_name="notebooklmlm",
            format_version=version,
            created_at=payload.get("created_at") or datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def load(cls, path: str | Path) -> "NotebookDocument":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Notebook document must contain a JSON object")
        return cls.from_dict(payload)
