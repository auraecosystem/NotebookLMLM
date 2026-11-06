# Security policy and execution boundaries

NotebookLMLM executes code and queries that can access data and system resources. Treat notebook documents, bookmark definitions, cell contents, and execution parameters as untrusted input unless their origin and permissions are verified.

## Current safeguards

- SQL values are passed as driver parameters. Do not construct SQL by concatenating user-provided values.
- SQLite connections use read-only URI mode by default.
- Python code runs in a separate interpreter process and has an execution timeout.
- Notebook and bookmark persistence stores definitions and metadata, not database credentials.

## Important limitations

A subprocess and timeout are not a security sandbox. Python code can still access files, environment variables, and the network with the operating-system permissions of the running user. Do not run untrusted Python code on a sensitive host.

Before exposing execution to multiple users or remote clients, implement:
1. OS/container/VM isolation with a non-privileged identity.
2. CPU, memory, process, disk, and wall-clock limits.
3. Filesystem and network allowlists/denylists.
4. Authentication, per-user authorization, and tenant isolation.
5. Secret injection outside notebook documents and logs.
6. Audit events for executions, data access, and administrative changes.
7. Explicit approval for destructive database operations.
8. Output size limits and safe rendering of HTML, SVG, and rich outputs.

## Database guidance

Keep SQLite read-only unless write access is explicitly required. For future database adapters, use parameterized statements, least-privilege credentials, TLS where applicable, and connection-level query timeouts. Bookmark names and descriptions are metadata; they are not authorization controls.
