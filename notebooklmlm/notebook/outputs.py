"""Cell output model."""
from dataclasses import dataclass,field
from typing import Any
@dataclass
class CellOutput:
    output_type:str; data:Any=None; stdout:str=""; stderr:str=""; metadata:dict[str,Any]=field(default_factory=dict)
