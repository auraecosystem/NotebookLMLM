"""Policy-gated execution shared by notebook cells and bookmarks."""
from typing import Any
from notebooklmlm.kernels.base import Kernel
from notebooklmlm.models import ExecutionResult
from notebooklmlm.security.permissions import ExecutionPolicy
from notebooklmlm.security.audit import AuditLogger
from .session import NotebookSession
class ExecutionService:
    def __init__(self,policy:ExecutionPolicy|None=None,audit:AuditLogger|None=None)->None:
        self.policy=policy or ExecutionPolicy(); self.audit=audit; self._kernels:dict[str,Kernel]={}
    def register_kernel(self,kernel:Kernel)->None:
        if kernel.language in self._kernels: raise ValueError(f"Kernel already registered: {kernel.language}")
        self._kernels[kernel.language]=kernel
    def execute(self,language:str,source:str,*,session:NotebookSession|None=None,context:dict[str,Any]|None=None)->ExecutionResult:
        if session: session.ensure_open()
        if not self.policy.allows(language): result=ExecutionResult(status="denied",stderr=f"Execution denied by policy for: {language}")
        elif language not in self._kernels: result=ExecutionResult(status="error",stderr=f"No kernel registered for language: {language}")
        else: result=self._kernels[language].execute(source,context)
        if session:
            session.state.execution_count+=1
            result=ExecutionResult(status=result.status,data=result.data,stdout=result.stdout,stderr=result.stderr,execution_count=session.state.execution_count,metadata=result.metadata)
        if self.audit: self.audit.record({"event":"kernel.execute","language":language,"status":result.status,"session_id":session.session_id if session else None})
        return result
    def close(self)->None:
        for kernel in self._kernels.values(): kernel.close()
