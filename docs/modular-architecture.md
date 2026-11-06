# Modular architecture

NotebookLMLM separates orchestration, reusable bookmarks, notebook documents, execution adapters, intelligence interfaces, database connectivity, and security controls.

- core: sessions, state, scheduling, engine lifecycle, and policy-gated execution.
- bookmarks: registry, manager, templates, typed variables, linked-table metadata, and version helpers.
- notebook: cells, outputs, metadata, document validation, and JSON serialization.
- kernels: Python and SQL adapters plus explicit JavaScript, R, Bash, and LMLM-Lang extension points.
- intelligence: provider-neutral assistant proposals, query generation, static analysis, error diagnosis, and workflow planning.
- database: connection registry and SQLite adapter.
- security: fail-closed language policy, secret lookup, audit events, and sandbox contract.
- api: transport-neutral package boundary.

## Security defaults

The engine defaults to SQL-only execution. Python subprocess execution is not a sandbox and must not be enabled for untrusted input. SandboxRunner refuses execution because no hardened OS/container backend is configured. AI-generated code and workflow plans are proposals and require review and explicit execution through the policy-gated service.

## Compatibility

Public imports remain supported: notebooklmlm.bookmarks.BookmarkRegistry, notebooklmlm.notebook.NotebookDocument, and notebooklmlm.kernels.python.PythonKernel. The original flat runtime.py API remains available.

## Not production-complete

Persistent Python sessions, remote database drivers, hardened OS/container isolation, quotas, API authentication/authorization, tenant isolation, and a web UI remain future work. Language directories other than Python and SQL are extension points only; they do not execute code yet.
