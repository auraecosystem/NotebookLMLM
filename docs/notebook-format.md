# Notebook document format

The initial format is UTF-8 JSON with:

- `format_name`: always `notebooklmlm`.
- `format_version`: currently `1`.
- `created_at`: UTC ISO-8601 timestamp.
- `metadata`: document-level metadata.
- `cells`: ordered cell objects.

Each cell contains a stable UUID, a `cell_type` (`markdown`, `code`, or `sql`), source text, output records, metadata, and an optional execution count.

Unknown future format versions are rejected rather than guessed. Add migrations before introducing incompatible schema changes.
