"""Environment-backed secret provider."""
import os
class EnvironmentSecretProvider:
    def get(self,name:str)->str:
        if not name or not name.replace("_","").isalnum(): raise ValueError("Invalid secret name")
        value=os.environ.get(name)
        if value is None: raise KeyError(f"Secret not found: {name}")
        return value
