"""
LayeredMemoryManager - Core implementation of the 4-layer memory architecture
"""
from typing import Dict, List, Any, Optional
from enum import Enum
import json
import time
from datetime import datetime
from .sqlite_dao import MemoryHubDAO


class MemoryLayer(Enum):
    """Memory layer classification"""
    SESSION = "session"     # Layer-1: Temporary in-memory
    CORE = "core"          # Layer-2: SQLite persistent
    APPLICATION = "app"     # Layer-3: JSONL files
    ARCHIVE = "archive"     # Layer-4: Compressed storage


class LayeredMemoryManager:
    """
    Layered memory management system implementing 4-layer architecture.
    
    This skeleton version uses in-memory storage only.
    Persistence layers (SQLite, JSONL, Archive) will be added in subsequent tasks.
    """
    
    def __init__(self, path: str = "./memoryhub_data"):
        """
        Initialize the memory manager.
        
        Args:
            path: Base path for persistent storage
        """
        self.path = path
        # In-memory storage for session layer
        self._session_memory: Dict[str, Any] = {}
        self._memory_counter = 0
        
        # SQLite DAO for Core layer persistence
        db_path = f"{path}/memory.db"
        self._dao = MemoryHubDAO(db_path)
        
        # Load existing Core memories from SQLite
        self._core_memory: Dict[str, Any] = {}
        self._load_core_memories()
        
        self._stats = {
            "memories_stored": 0,
            "memories_recalled": 0,
            "layers_loaded": ["session", "core"],
            "created_at": datetime.now().isoformat()
        }
    
    def remember(self, content: str, tags: List[str], context_path: str = "") -> Dict[str, Any]:
        """
        Store a memory in the appropriate layer.
        
        Args:
            content: The content to store
            tags: List of tags for categorization
            context_path: Context path for the memory
            
        Returns:
            Dictionary containing the stored memory record
        """
        # Generate memory ID
        self._memory_counter += 1
        memory_id = f"mem_{self._memory_counter}"
        
        # Classify memory layer
        layer = self._classify_memory(content, tags)
        
        # Create memory record
        memory_record = {
            "id": memory_id,
            "content": content,
            "tags": tags,
            "context_path": context_path,
            "layer": layer.value,
            "created_at": datetime.now().isoformat(),
            "recalled_count": 0
        }
        
        # Store in appropriate layer
        if layer == MemoryLayer.SESSION:
            self._session_memory[memory_id] = memory_record
        elif layer == MemoryLayer.CORE:
            # Store in SQLite for persistence
            if self._dao.store_memory(memory_record):
                self._core_memory[memory_id] = memory_record
            else:
                # Fallback to session if SQLite fails
                self._session_memory[memory_id] = memory_record
        else:
            # For APPLICATION and ARCHIVE layers, store in session for now
            # Will be implemented in core-02c, core-02d
            self._session_memory[memory_id] = memory_record
        
        # Update stats
        self._stats["memories_stored"] += 1
        
        return memory_record
    
    def recall(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve memories matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching memory records
        """
        results = []
        query_lower = query.lower()
        
        # Search in Core layer (SQLite) first
        core_results = self._dao.search_memories(query, "core", limit)
        for memory in core_results:
            # Update recall count in database
            self._dao.update_recall_count(memory["id"])
            results.append(memory)
            
            if len(results) >= limit:
                return results
        
        # Search in session memory if we need more results
        remaining_limit = limit - len(results)
        if remaining_limit > 0:
            for memory_id, memory in self._session_memory.items():
                # Simple text matching
                if (query_lower in memory["content"].lower() or 
                    any(query_lower in tag.lower() for tag in memory["tags"]) or
                    query_lower in memory["context_path"].lower()):
                    
                    # Update recall stats
                    memory["recalled_count"] += 1
                    results.append(memory.copy())
                    
                    if len(results) >= limit:
                        break
        
        # Update global recall stats
        self._stats["memories_recalled"] += len(results)
        
        # Sort by creation time (most recent first)
        results.sort(key=lambda x: x["created_at"], reverse=True)
        
        return results
    
    def stats(self) -> Dict[str, Any]:
        """
        Get memory system statistics.
        
        Returns:
            Dictionary containing system statistics
        """
        current_stats = self._stats.copy()
        
        # Get database stats
        db_stats = self._dao.get_stats()
        
        current_stats.update({
            "session_memory_count": len(self._session_memory),
            "core_memory_count": len(self._core_memory),
            "app_memory_count": 0,   # Will be implemented in core-02c
            "archive_memory_count": 0,  # Will be implemented in core-02d
            "db_stats": db_stats
        })
        return current_stats
    
    def load_layer(self, layer: str, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load a specific memory layer.
        
        Args:
            layer: Layer name to load ("session", "core", "app", "archive")
            force_reload: Whether to force reload the layer
            
        Returns:
            Dictionary containing layer information
        """
        if layer == "session":
            return {
                "layer": "session",
                "count": len(self._session_memory),
                "loaded": True,
                "memory_ids": list(self._session_memory.keys())
            }
        elif layer == "core":
            if force_reload:
                self._load_core_memories()
            return {
                "layer": "core",
                "count": len(self._core_memory),
                "loaded": True,
                "memory_ids": list(self._core_memory.keys())
            }
        else:
            # Placeholder for APPLICATION and ARCHIVE layers
            return {
                "layer": layer,
                "count": 0,
                "loaded": False,
                "memory_ids": []
            }
    
    def _classify_memory(self, content: str, tags: List[str]) -> MemoryLayer:
        """
        Classify memory into appropriate layer based on content and tags.
        
        Args:
            content: Memory content
            tags: Memory tags
            
        Returns:
            MemoryLayer enum indicating the appropriate layer
        """
        content_lower = content.lower()
        tags_lower = [tag.lower() for tag in tags]
        
        # Classification rules per design document
        if "task_id" in content_lower or "window_id" in content_lower:
            return MemoryLayer.CORE
        elif "log" in content_lower or "trace" in content_lower:
            return MemoryLayer.APPLICATION
        elif "archive" in tags_lower:
            return MemoryLayer.ARCHIVE
        else:
            return MemoryLayer.SESSION
    
    def _load_core_memories(self):
        """Load Core layer memories from SQLite database"""
        try:
            memories = self._dao.load_memories("core")
            self._core_memory.clear()
            for memory in memories:
                self._core_memory[memory["id"]] = memory
        except Exception as e:
            print(f"Warning: Failed to load core memories: {e}")
            self._core_memory = {}