"""
Memory Extension Plugin - Advanced persistent memory management
"""
from typing import Dict, Any, List
import json
import os

class MemoryExtension:
    def __init__(self, storage_path: str = "memory_store.json"):
        self.storage_path = storage_path
        self.memory: Dict[str, Any] = self._load_memory()
        self.short_term: List[str] = []
        self.long_term: Dict[str, Any] = {}
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load persistent memory from storage"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_memory(self) -> None:
        """Persist memory to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def remember(self, key: str, value: Any, long_term: bool = False) -> None:
        """Store information in memory"""
        if long_term:
            self.long_term[key] = value
        else:
            self.short_term.append(f"{key}: {value}")
            if len(self.short_term) > 100:
                self.short_term.pop(0)
        
        self.memory[key] = value
        self.save_memory()
    
    def recall(self, key: str, default: Any = None) -> Any:
        """Retrieve information from memory"""
        return self.memory.get(key, default)
    
    def forget(self, key: str) -> None:
        """Remove information from memory"""
        if key in self.memory:
            del self.memory[key]
            self.save_memory()
