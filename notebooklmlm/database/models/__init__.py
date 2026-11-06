"""Database configuration models."""
from dataclasses import dataclass,field
from typing import Any
@dataclass(frozen=True)
class DatabaseConfig:
    alias:str
    driver:str
    options:dict[str,Any]=field(default_factory=dict)
    secret_ref:str|None=None
    def __post_init__(self)->None:
        if not self.alias or not self.driver: raise ValueError("Database alias and driver are required")
        if any(key.lower() in {"password","secret","token","api_key"} for key in self.options):
            raise ValueError("Secrets must be supplied through secret_ref, not inline options")
