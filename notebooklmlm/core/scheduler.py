"""Bounded thread scheduler for asynchronous orchestration."""
from concurrent.futures import Future,ThreadPoolExecutor
from typing import Any,Callable
class ExecutionScheduler:
    def __init__(self,max_workers:int=2)->None:
        if max_workers<1: raise ValueError("max_workers must be positive")
        self._pool=ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix="notebooklmlm"); self._closed=False
    def submit(self,fn:Callable[...,Any],*args:Any,**kwargs:Any)->Future:
        if self._closed: raise RuntimeError("Scheduler is closed")
        return self._pool.submit(fn,*args,**kwargs)
    def close(self,wait:bool=True)->None:
        if not self._closed: self._closed=True; self._pool.shutdown(wait=wait,cancel_futures=True)
