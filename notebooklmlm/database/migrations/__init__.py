"""Database migration extension point."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
@dataclass(frozen=True)
class Migration:
    version:int
    name:str
    statements:tuple[str,...]
class MigrationBackend(Protocol):
    def current_version(self)->int: ...
    def apply(self,migration:Migration)->None: ...
class MigrationRunner:
    def __init__(self,backend:MigrationBackend)->None: self.backend=backend
    def migrate(self,migrations:list[Migration])->int:
        current=self.backend.current_version()
        for item in sorted(migrations,key=lambda value:value.version):
            if item.version<=current: continue
            if item.version!=current+1: raise ValueError("Migrations must be contiguous and sequential")
            self.backend.apply(item); current=item.version
        return current
