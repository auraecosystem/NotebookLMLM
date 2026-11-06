"""Bookmark operations facade."""
from typing import Any
from .registry import Bookmark,BookmarkRegistry
class BookmarkManager:
    def __init__(self,registry:BookmarkRegistry)->None: self.registry=registry
    def save(self,name:str,query:str,**options:Any)->Bookmark: return self.registry.add(name,query,**options)
    def resolve(self,name:str,values:dict[str,Any]|None=None)->tuple[Bookmark,dict[str,Any]]:
        item=self.registry.get(name); params=values or {}; self.registry.validate_parameters(item,params); return item,params
