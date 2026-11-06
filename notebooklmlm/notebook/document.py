"""Versioned notebook document model, retaining the original JSON format."""
from dataclasses import asdict,dataclass,field
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
from .cells import CellType,NotebookCell
from .serialization import dump_document,load_document
@dataclass
class NotebookDocument:
    cells:list[NotebookCell]=field(default_factory=list); metadata:dict[str,Any]=field(default_factory=dict); format_name:str="notebooklmlm"; format_version:int=1; created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    def add_cell(self,cell_type:CellType,source:str)->NotebookCell:
        if cell_type not in ("markdown","code","sql"): raise ValueError(f"Unsupported cell type: {cell_type}")
        cell=NotebookCell(cell_type,source); self.cells.append(cell); return cell
    def to_dict(self)->dict[str,Any]: return asdict(self)
    def save(self,path:str|Path)->None: dump_document(self.to_dict(),path)
    @classmethod
    def from_dict(cls,payload:dict[str,Any])->"NotebookDocument":
        if payload.get("format_name")!="notebooklmlm": raise ValueError("Not a NotebookLMLM document")
        version=payload.get("format_version")
        if version!=1: raise ValueError(f"Unsupported notebook format version: {version}")
        return cls(cells=[NotebookCell(**item) for item in payload.get("cells",[])],metadata=payload.get("metadata",{}),format_version=version,created_at=payload.get("created_at") or datetime.now(timezone.utc).isoformat())
    @classmethod
    def load(cls,path:str|Path)->"NotebookDocument": return cls.from_dict(load_document(path))
