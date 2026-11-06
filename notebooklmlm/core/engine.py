"""High-level notebook engine."""
from notebooklmlm.kernels.base import Kernel
from notebooklmlm.security.permissions import ExecutionPolicy
from .execution import ExecutionService
from .scheduler import ExecutionScheduler
from .session import NotebookSession
class NotebookEngine:
    def __init__(self,*,policy:ExecutionPolicy|None=None,max_workers:int=2)->None:
        self.execution=ExecutionService(policy=policy); self.scheduler=ExecutionScheduler(max_workers); self._sessions:dict[str,NotebookSession]={}
    def register_kernel(self,kernel:Kernel)->None: self.execution.register_kernel(kernel)
    def create_session(self)->NotebookSession:
        session=NotebookSession(); self._sessions[session.session_id]=session; return session
    def close_session(self,session_id:str)->None: self._sessions.pop(session_id).close()
    def close(self)->None:
        self.scheduler.close(); self.execution.close()
        for session in self._sessions.values(): session.close()
        self._sessions.clear()
