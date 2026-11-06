"""Append-only JSONL audit logger."""
import json,os
from pathlib import Path
from threading import Lock
class AuditLogger:
    def __init__(self,path:str|Path)->None: self.path=Path(path); self._lock=Lock()
    def record(self,event:dict)->None:
        self.path.parent.mkdir(parents=True,exist_ok=True); line=(json.dumps(event,sort_keys=True,default=str)+"\n").encode()
        with self._lock:
            fd=os.open(self.path,os.O_APPEND|os.O_CREAT|os.O_WRONLY,0o600)
            try: os.write(fd,line)
            finally: os.close(fd)
