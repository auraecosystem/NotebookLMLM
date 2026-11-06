"""Execution error diagnostics."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ErrorDiagnosis:
    category:str; message:str; suggestion:str="Inspect the source and execution context."
class ErrorAnalyzer:
    def analyze(self,error:str)->ErrorDiagnosis:
        text=error.strip(); return ErrorDiagnosis("timeout" if "timed out" in text.lower() else "execution",text or "Unknown execution error")
