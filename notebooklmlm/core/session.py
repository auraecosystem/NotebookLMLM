"""Notebook session lifecycle."""
from dataclasses import dataclass,field
from datetime import datetime,timezone
from uuid import uuid4
from .state import SessionState
@dataclass
class NotebookSession:
    session_id:str=field(default_factory=lambda:str(uuid4()))
    state:SessionState=field(default_factory=SessionState)
    created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    closed:bool=False
    def ensure_open(self)->None:
        if self.closed: raise RuntimeError("Notebook session is closed")
    def close(self)->None:
        self.closed=True; self.state.namespace.clear(); self.state.variables.clear()
