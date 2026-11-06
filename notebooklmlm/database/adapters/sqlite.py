"""SQLite connection factory."""
import sqlite3
from pathlib import Path
class SQLiteAdapter:
    def connect(self,database:str|Path,*,read_only:bool=True,timeout:float=5.0)->sqlite3.Connection:
        if read_only: return sqlite3.connect(Path(database).resolve().as_uri()+"?mode=ro",uri=True,timeout=timeout)
        return sqlite3.connect(str(database),timeout=timeout)
