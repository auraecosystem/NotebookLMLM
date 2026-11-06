"""Bookmark version helpers."""
from .registry import Bookmark
def next_version(current:Bookmark|None)->int: return 1 if current is None else current.version+1
