"""Sandbox contract; refuses untrusted execution without a real backend."""
from dataclasses import dataclass
@dataclass(frozen=True)
class SandboxProfile:
    filesystem:str="deny-by-default"; network:str="disabled"; memory_limit_mb:int=256; cpu_seconds:int=5
    @property
    def enforced(self)->bool: return False
class SandboxUnavailable(RuntimeError): pass
class SandboxRunner:
    def run(self,*args,**kwargs): raise SandboxUnavailable("No OS/container sandbox backend configured; refusing untrusted execution")
