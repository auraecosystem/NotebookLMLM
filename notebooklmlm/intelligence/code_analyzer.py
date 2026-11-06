"""Minimal static-analysis extension point."""
from dataclasses import dataclass
@dataclass(frozen=True)
class AnalysisFinding:
    severity:str; message:str; line:int|None=None
class CodeAnalyzer:
    def analyze(self,source:str,language:str)->list[AnalysisFinding]:
        if language=="python" and "eval(" in source: return [AnalysisFinding("warning","Dynamic eval detected")]
        return []
