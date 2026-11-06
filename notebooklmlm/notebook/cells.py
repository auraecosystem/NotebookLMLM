"""Notebook cell model."""
from dataclasses import dataclass,field
from typing import Any,Literal
from uuid import uuid4
CellType=Literal["markdown","code","sql"]
@dataclass
class NotebookCell:
    cell_type:CellType; source:str; id:str=field(default_factory=lambda:str(uuid4())); outputs:list[dict[str,Any]]=field(default_factory=list); metadata:dict[str,Any]=field(default_factory=dict); execution_count:int|None=None
