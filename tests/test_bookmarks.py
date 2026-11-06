import pytest

from notebooklmlm.bookmarks import BookmarkRegistry, required_parameters


def test_bookmark_persists_and_versions(tmp_path):
    path = tmp_path / "bookmarks.db"
    with BookmarkRegistry(path) as registry:
        first = registry.add("customer-search", "SELECT * FROM customers WHERE id = :id")
        second = registry.add("customer-search", "SELECT id FROM customers WHERE id = :id", replace=True)
        assert first.version == 1
        assert second.version == 2
    with BookmarkRegistry(path) as registry:
        assert registry.get("customer-search").version == 2


def test_duplicate_and_invalid_names_are_rejected(tmp_path):
    with BookmarkRegistry(tmp_path / "bookmarks.db") as registry:
        registry.add("valid_name", "SELECT 1")
        with pytest.raises(ValueError):
            registry.add("valid_name", "SELECT 2")
        with pytest.raises(ValueError):
            registry.add("not valid", "SELECT 1")


def test_parameter_discovery_and_validation(tmp_path):
    assert required_parameters("SELECT * FROM t WHERE id=:id AND name=:name") == {"id", "name"}
    with BookmarkRegistry(tmp_path / "bookmarks.db") as registry:
        bookmark = registry.add("lookup", "SELECT * FROM t WHERE id=:id")
        registry.validate_parameters(bookmark, {"id": 3})
        with pytest.raises(ValueError):
            registry.validate_parameters(bookmark, {})
