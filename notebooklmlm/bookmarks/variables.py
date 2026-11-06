"""Typed variable validation; values remain separate from source text."""
from typing import Any
def validate_variables(schema:dict[str,dict[str,Any]],values:dict[str,Any])->None:
    missing={k for k,v in schema.items() if v.get("required",False) and k not in values}; extra=set(values)-set(schema)
    if missing: raise ValueError(f"Missing variables: {', '.join(sorted(missing))}")
    if extra: raise ValueError(f"Unexpected variables: {', '.join(sorted(extra))}")
    checks={"string":str,"integer":int,"number":(int,float),"boolean":bool}
    for key,value in values.items():
        kind=schema[key].get("type")
        if kind in checks and (not isinstance(value,checks[kind]) or (kind=="integer" and isinstance(value,bool))): raise ValueError(f"Variable {key!r} must be {kind}")
def resolve_variables(schema:dict[str,dict[str,Any]],values:dict[str,Any])->dict[str,Any]:
    validate_variables(schema,values); return dict(values)
