"""Query proposal model; never executes generated SQL."""
from dataclasses import dataclass
@dataclass(frozen=True)
class QueryProposal:
    query:str; parameters:tuple[str,...]=()
