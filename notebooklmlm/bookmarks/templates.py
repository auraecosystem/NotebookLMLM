"""Reusable query template model."""
from dataclasses import dataclass,field
from typing import Any
@dataclass(frozen=True)
class BookmarkTemplate:
    source:str; language:str="sql"; description:str=""; parameter_schema:dict[str,dict[str,Any]]=field(default_factory=dict)
