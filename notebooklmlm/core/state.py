"""Session-scoped runtime state."""
from dataclasses import dataclass,field
from typing import Any
@dataclass
class SessionState:
    namespace:dict[str,Any]=field(default_factory=dict)
    execution_count:int=0
    variables:dict[str,Any]=field(default_factory=dict)
    metadata:dict[str,Any]=field(default_factory=dict)
    def snapshot(self)->dict[str,Any]: return {"execution_count":self.execution_count,"variables":dict(self.variables),"metadata":dict(self.metadata)}
