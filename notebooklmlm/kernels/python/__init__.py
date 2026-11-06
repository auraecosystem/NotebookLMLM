"""One-shot Python kernel; subprocess execution is not a security sandbox."""
import json,subprocess,sys
from typing import Any
from notebooklmlm.kernels.base import Kernel
from notebooklmlm.models import ExecutionResult
_WORKER='''import contextlib,io,json,sys\np=json.loads(sys.stdin.read()); o=io.StringIO(); e=io.StringIO(); n={"__name__":"__main__"}\ntry:\n with contextlib.redirect_stdout(o),contextlib.redirect_stderr(e): exec(compile(p["code"],"<notebook-cell>","exec"),n,n)\n r={"status":"ok","stdout":o.getvalue(),"stderr":e.getvalue()}\nexcept BaseException as x: r={"status":"error","stdout":o.getvalue(),"stderr":e.getvalue()+type(x).__name__+": "+str(x)}\nsys.stdout.write(json.dumps(r))'''
class PythonKernel(Kernel):
    language="python"
    def __init__(self,timeout:float=5.0,max_output_bytes:int=1_000_000)->None:
        if timeout<=0 or max_output_bytes<1: raise ValueError("timeout and output limit must be positive")
        self.timeout,self.max_output_bytes=timeout,max_output_bytes
    def execute(self,code:str,context:dict[str,Any]|None=None)->ExecutionResult:
        if context: return ExecutionResult(status="error",stderr="Python context injection is not supported")
        try: p=subprocess.run([sys.executable,"-I","-c",_WORKER],input=json.dumps({"code":code}),text=True,capture_output=True,timeout=self.timeout,check=False)
        except subprocess.TimeoutExpired: return ExecutionResult(status="error",stderr=f"Execution timed out after {self.timeout} seconds")
        if len(p.stdout.encode("utf-8"))>self.max_output_bytes: return ExecutionResult(status="error",stderr="Python output exceeded configured limit")
        try: data=json.loads(p.stdout)
        except json.JSONDecodeError: return ExecutionResult(status="error",stderr=p.stderr or "Python worker returned invalid output")
        return ExecutionResult(status=data["status"],stdout=data.get("stdout",""),stderr=data.get("stderr",""),metadata={"returncode":p.returncode})
