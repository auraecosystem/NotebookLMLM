"""Command-line tools for NoteBookmarks."""

from __future__ import annotations

import argparse
import json

from notebooklmlm.bookmarks import BookmarkRegistry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="notebooklmlm")
    parser.add_argument("--database", default="notebooklmlm.db")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("bookmark-add")
    add.add_argument("name")
    add.add_argument("query")
    add.add_argument("--description", default="")
    add.add_argument("--language", default="sql")
    commands.add_parser("bookmark-list")
    delete = commands.add_parser("bookmark-delete")
    delete.add_argument("name")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    with BookmarkRegistry(args.database) as registry:
        if args.command == "bookmark-add":
            item = registry.add(args.name, args.query, args.description, args.language)
            print(json.dumps(item.__dict__, indent=2))
        elif args.command == "bookmark-list":
            print(json.dumps([item.__dict__ for item in registry.list()], indent=2))
        elif args.command == "bookmark-delete":
            if not registry.delete(args.name):
                raise SystemExit(f"Bookmark not found: {args.name}")
            print(f"Deleted bookmark: {args.name}")


if __name__ == "__main__":
    main()
