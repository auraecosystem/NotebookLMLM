# NoteBookmarks

NoteBookmarks is an independently usable query-template registry backed by SQLite.

## Create a bookmark

```python
from notebooklmlm.bookmarks import BookmarkRegistry

with BookmarkRegistry("notebooklmlm.db") as registry:
    saved = registry.add(
        name="customer-search",
        query="SELECT id, name FROM customers WHERE name LIKE :pattern",
        description="Search customers by name",
        parameters={"pattern": {"type": "string", "required": True}},
    )
    print(saved.version)
```

## Resolve and validate parameters

```python
with BookmarkRegistry("notebooklmlm.db") as registry:
    bookmark = registry.get("customer-search")
    values = {"pattern": "%Ada%"}
    registry.validate_parameters(bookmark, values)
```

Pass `bookmark.query` and the validated values separately to a database driver's parameter-binding API. Never interpolate variable values into SQL strings.

The initial parameter-name discovery helper is intentionally lightweight; it does not parse SQL grammar and may see colon-like tokens inside literals or comments. The database driver remains authoritative for statement parsing and parameter binding.
