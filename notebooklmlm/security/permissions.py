"""Fail-closed language policy."""
from dataclasses import dataclass,field
@dataclass(frozen=True)
class ExecutionPolicy:
    allowed_languages:frozenset[str]=field(default_factory=lambda:frozenset({"sql"}))
    def allows(self,language:str)->bool: return language in self.allowed_languages
