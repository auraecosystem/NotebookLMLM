"""Workflow planning produces proposals, not side effects."""
from dataclasses import dataclass
@dataclass(frozen=True)
class WorkflowStep:
    name:str; action:str; requires_confirmation:bool=True
class WorkflowPlanner:
    def plan(self,actions:list[str])->list[WorkflowStep]: return [WorkflowStep(f"step-{i+1}",action) for i,action in enumerate(actions)]
