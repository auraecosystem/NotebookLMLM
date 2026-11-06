# NotebookLMLM

NotebookLMLM is an extensible computational notebook foundation combining reusable query bookmarks with a multi-language notebook runtime.

## Included foundation

- Versioned JSON notebook documents with Markdown, code, and SQL cells.
- Persistent NoteBookmarks registry backed by SQLite.
- Named SQL parameters bound by the database driver, never interpolated into SQL text.
- SQLite SQL kernel with read-only mode enabled by default.
- Python execution through a separate subprocess with a configurable timeout.
- Shared runtime interface and command-line entry point.
- Tests for bookmark persistence, parameter binding, notebook serialization, and runtime behavior.

## Requirements

- Python 3.10+
- No runtime third-party dependencies

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
notebooklmlm bookmark-add customer-search "SELECT id, name FROM customers WHERE name LIKE :pattern" --description "Find customers by name"
notebooklmlm bookmark-list
python -m pytest
```

## Python API

```python
from notebooklmlm.bookmarks import BookmarkRegistry
from notebooklmlm.kernels.sqlite import SQLiteKernel

registry = BookmarkRegistry("notebooklmlm.db")
bookmark = registry.get("customer-search")
kernel = SQLiteKernel("app.db", read_only=True)
registry.validate_parameters(bookmark, {"pattern": "%Ada%"})
result = kernel.execute(bookmark.query, {"pattern": "%Ada%"})
print(result.data)
kernel.close()
registry.close()
```

## Architecture

- `notebooklmlm.notebook`: notebook document and cell model.
- `notebooklmlm.bookmarks`: persistent query-template registry.
- `notebooklmlm.kernels`: language-specific execution adapters.
- `notebooklmlm.runtime`: shared execution facade.

The Python kernel launches a fresh interpreter for each execution. This provides process separation and timeout control, but it is **not a complete security sandbox**. Do not execute untrusted code with it. Production deployments must add OS/container isolation, resource limits, filesystem controls, network policy, authentication, and authorization.

The SQLite kernel is read-only by default. Enable writes explicitly only for trusted workflows. Database credentials and secrets should be supplied by a secret manager or environment, never embedded in notebooks or bookmarks.

## Current scope

This is a dependency-light MVP foundation. It does not yet claim production-grade multi-user sessions, persistent Python kernel state, remote database drivers, a web UI, or LMLM model integration. Those should be added behind the documented interfaces with tests and explicit security boundaries.

See [SECURITY.md](SECURITY.md) for execution and data-handling guidance.
