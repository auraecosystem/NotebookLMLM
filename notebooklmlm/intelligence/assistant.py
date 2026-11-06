"""Assistant proposals require explicit review before execution."""
from dataclasses import dataclass,field
from typing import Any,Protocol
@dataclass(frozen=True)
class AssistantProposal:
    kind:str; content:str; requires_confirmation:bool=True; metadata:dict[str,Any]=field(default_factory=dict)
class AssistantProvider(Protocol):
    def propose(self,prompt:str,context:dict[str,Any]|None=None)->AssistantProposal: ...
