"""Notebook metadata model."""
from dataclasses import dataclass,field
from typing import Any
@dataclass
class NotebookMetadata:
    title:str=""; kernelspec:dict[str,Any]=field(default_factory=dict); tags:list[str]=field(default_factory=list); custom:dict[str,Any]=field(default_factory=dict)
