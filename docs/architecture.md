# Architecture

NotebookLMLM is organized around two cooperating subsystems:

1. **NoteBookmarks** stores reusable query and code templates independently of notebook documents.
2. **Notebook Engine** stores ordered cells and delegates executable cells to language kernels.

Both use a shared runtime result contract so frontends and future orchestration services do not need language-specific result handling.

## Component boundaries

| Package | Responsibility |
| --- | --- |
| `notebook` | Versioned document format, cell metadata, serialization |
| `bookmarks` | Persistent bookmark CRUD, version increments, parameter metadata |
| `kernels.base` | Common kernel lifecycle and execution interface |
| `kernels.sqlite` | SQLite execution with bound parameters and read-only default |
| `kernels.python` | One-shot subprocess execution and timeout |
| `runtime` | Kernel registration, dispatch, execution counts, normalized results |
| `models` | Shared result data model |
| `cli` | Initial bookmark management commands |

## Execution lifecycle

1. A client selects a notebook cell or saved bookmark.
2. The caller resolves and validates the requested language and parameters.
3. The runtime dispatches source to the registered kernel.
4. The kernel returns an `ExecutionResult`.
5. The client persists the result in the cell output and execution history.

The runtime deliberately does not silently execute a bookmark when a table is opened. A future table-browser integration should make that behavior explicit, visible, and permission-checked.

## Extension points

Implement additional language kernels by subclassing `Kernel`. Implement additional database engines behind a database adapter rather than embedding vendor-specific connection logic in the notebook document model.

Future LMLM integration belongs in an orchestration/service layer. The model may propose code or workflows, but all execution must pass through the same policy and runtime boundaries as user-authored cells.
