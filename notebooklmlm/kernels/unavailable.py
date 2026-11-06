"""Fail-closed placeholder for kernels without a reviewed worker."""
from typing import Any
from notebooklmlm.kernels.base import Kernel
from notebooklmlm.models import ExecutionResult
class UnavailableKernel(Kernel):
    language="unavailable"
    def execute(self,code:str,context:dict[str,Any]|None=None)->ExecutionResult: return ExecutionResult(status="unavailable",stderr=f"The {self.language} kernel is not installed or enabled")
