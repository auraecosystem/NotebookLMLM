"""JSON document serialization helpers."""
import json
from pathlib import Path
from typing import Any
def dump_document(payload:dict[str,Any],path:str|Path)->None:
    target=Path(path); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def load_document(path:str|Path)->dict[str,Any]:
    payload=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload,dict): raise ValueError("Notebook document must contain a JSON object")
    return payload
