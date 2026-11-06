# NotebookLMLM

NotebookLMLM combines a reusable NoteBookmarks query registry with a modular computational notebook engine.

## Architecture

The codebase is organized into explicit layers:

- notebooklmlm/core: engine, execution service, scheduler, session, and state.
- notebooklmlm/bookmarks: registry, manager, templates, variables, linked tables, and versioning.
- notebooklmlm/notebook: document, cells, outputs, metadata, and serialization.
- notebooklmlm/kernels: Python and SQLite SQL implementations; JavaScript, R, Bash, and LMLM-Lang extension points.
- notebooklmlm/intelligence: assistant proposal interfaces, query generation, code/error analysis, and workflow planning.
- notebooklmlm/database: connection registry and SQLite adapter.
- notebooklmlm/security: execution policy, sandbox contract, secrets, and audit logging.
- notebooklmlm/api: transport-neutral API boundary.

See docs/modular-architecture.md for component boundaries and security limitations.

## Quick start

Requirements: Python 3.10+. The runtime has no mandatory third-party dependencies.

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

with BookmarkRegistry("notebooklmlm.db") as registry:
    bookmark = registry.get("customer-search")
    registry.validate_parameters(bookmark, {"pattern": "%Ada%"})
    kernel = SQLiteKernel("app.db", read_only=True)
    try:
        result = kernel.execute(bookmark.query, {"pattern": "%Ada%"})
        print(result.data)
    finally:
        kernel.close()
```

## Execution and security

The new NotebookEngine defaults to a fail-closed policy that allows SQL only. Python must be explicitly enabled by a deployment policy. The Python kernel starts a fresh subprocess for each execution; process separation and timeouts are not a complete sandbox. Do not run untrusted code with it.

SandboxRunner deliberately refuses execution until a real OS/container isolation backend is configured. JavaScript, R, Bash, and LMLM-Lang are extension points only; no worker is enabled for them yet. AI-generated code and workflow plans are proposals, not automatically executed actions.

SQLite is read-only by default. SQL values must be passed as bound parameters, never interpolated into query strings. Secrets should be obtained from a secret provider and must not be stored in notebooks or bookmarks.

## Scope

This is an extensible foundation, not a claim of production readiness. Persistent Python sessions, hardened sandboxing, resource quotas, remote database drivers, API authentication/authorization, tenant isolation, a web UI, and LMLM model integration remain future implementation gates.

See SECURITY.md for the execution threat model.
