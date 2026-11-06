"""Explicit bookmark-to-table metadata registry."""
from dataclasses import dataclass
@dataclass(frozen=True)
class LinkedTable:
    bookmark_name:str; table_name:str; database_alias:str="default"
class LinkedTableRegistry:
    def __init__(self)->None: self._items:dict[tuple[str,str],LinkedTable]={}
    def link(self,bookmark_name:str,table_name:str,database_alias:str="default")->LinkedTable:
        if not bookmark_name or not table_name: raise ValueError("bookmark_name and table_name are required")
        item=LinkedTable(bookmark_name,table_name,database_alias); self._items[(bookmark_name,table_name)]=item; return item
    def for_bookmark(self,name:str)->list[LinkedTable]: return [v for v in self._items.values() if v.bookmark_name==name]
    def unlink(self,name:str,table:str)->bool: return self._items.pop((name,table),None) is not None
