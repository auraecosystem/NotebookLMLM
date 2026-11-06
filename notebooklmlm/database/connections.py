"""Named database connection registry."""
class ConnectionRegistry:
    def __init__(self)->None: self._connections={}
    def register(self,name:str,connection)->None:
        if not name or name in self._connections: raise ValueError("Connection name must be unique and non-empty")
        self._connections[name]=connection
    def get(self,name:str): return self._connections[name]
    def close(self)->None:
        for item in self._connections.values():
            close=getattr(item,"close",None)
            if callable(close): close()
        self._connections.clear()
