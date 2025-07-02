"""
LayeredMemoryManager - Core implementation of the 4-layer memory architecture
"""
from typing import Dict, List, Any, Optional
from enum import Enum
import json
import time
from datetime import datetime
from .sqlite_dao import MemoryHubDAO
from .jsonl_dao import JSONLMemoryDAO


class MemoryLayer(Enum):
    """Memory layer classification"""
    SESSION = "session"     # Layer-1: Temporary in-memory
    CORE = "core"          # Layer-2: SQLite persistent
    APPLICATION = "application"     # Layer-3: JSONL files
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
        
        # JSONL DAO for Application and Archive layers
        self._jsonl_dao = JSONLMemoryDAO(path)
        
        # Load existing Core memories from SQLite
        self._core_memory: Dict[str, Any] = {}
        self._load_core_memories()
        
        # Load Application and Archive memories from JSONL
        self._app_memory: Dict[str, Any] = {}
        self._archive_memory: Dict[str, Any] = {}
        self._load_jsonl_memories()
        
        self._stats = {
            "memories_stored": 0,
            "memories_recalled": 0,
            "layers_loaded": ["session", "core", "application", "archive"],
            "created_at": datetime.now().isoformat(),
            "recall_latencies": [],  # Track recall latencies for performance analysis
            "total_recall_time": 0.0  # Total time spent on recalls
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
        elif layer == MemoryLayer.APPLICATION:
            # Store in JSONL for application logs
            if self._jsonl_dao.store_memory(memory_record, "application"):
                self._app_memory[memory_id] = memory_record
            else:
                # Fallback to session if JSONL fails
                self._session_memory[memory_id] = memory_record
        elif layer == MemoryLayer.ARCHIVE:
            # Store in JSONL for archive
            if self._jsonl_dao.store_memory(memory_record, "archive"):
                self._archive_memory[memory_id] = memory_record
            else:
                # Fallback to session if JSONL fails
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
        start_time = time.time()
        results = []
        query_lower = query.lower()
        
        # Search priority: Core > Application > Archive > Session
        
        # 1. Search in Core layer (SQLite) first - highest priority
        core_results = self._dao.search_memories(query, "core", limit)
        for memory in core_results:
            # Update recall count in database
            self._dao.update_recall_count(memory["id"])
            results.append(memory)
            
            if len(results) >= limit:
                return results
        
        # 2. Search in Application layer (JSONL) 
        remaining_limit = limit - len(results)
        if remaining_limit > 0:
            app_results = self._jsonl_dao.search_memories(query, "application", remaining_limit)
            for memory in app_results:
                # Update recall count in JSONL
                self._jsonl_dao.update_recall_count(memory["id"], "application")
                results.append(memory)
                
                if len(results) >= limit:
                    return results
        
        # 3. Search in Archive layer (JSONL)
        remaining_limit = limit - len(results)
        if remaining_limit > 0:
            archive_results = self._jsonl_dao.search_memories(query, "archive", remaining_limit)
            for memory in archive_results:
                # Update recall count in JSONL
                self._jsonl_dao.update_recall_count(memory["id"], "archive")
                results.append(memory)
                
                if len(results) >= limit:
                    return results
        
        # 4. Search in session memory if we need more results
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
        
        # Calculate recall latency
        end_time = time.time()
        recall_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Update global recall stats
        self._stats["memories_recalled"] += len(results)
        self._stats["recall_latencies"].append(recall_time)
        self._stats["total_recall_time"] += recall_time
        
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
        
        # Get JSONL stats
        jsonl_stats = self._jsonl_dao.get_stats()
        
        # Calculate performance metrics
        latencies = self._stats["recall_latencies"]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        max_latency = max(latencies) if latencies else 0.0
        min_latency = min(latencies) if latencies else 0.0
        
        # Calculate total memories across all layers
        total_memories = (len(self._session_memory) + len(self._core_memory) + 
                         len(self._app_memory) + len(self._archive_memory))
        
        current_stats.update({
            "session_memory_count": len(self._session_memory),
            "core_memory_count": len(self._core_memory),
            "app_memory_count": len(self._app_memory),
            "archive_memory_count": len(self._archive_memory),
            "total_memories": total_memories,
            "performance": {
                "avg_recall_latency_ms": round(avg_latency, 2),
                "max_recall_latency_ms": round(max_latency, 2),
                "min_recall_latency_ms": round(min_latency, 2),
                "total_recall_time_ms": round(self._stats["total_recall_time"], 2),
                "recall_count": len(latencies)
            },
            "db_stats": db_stats,
            "jsonl_stats": jsonl_stats
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
        elif layer == "app" or layer == "application":
            if force_reload:
                self._load_jsonl_memories()
            return {
                "layer": "application",
                "count": len(self._app_memory),
                "loaded": True,
                "memory_ids": list(self._app_memory.keys())
            }
        elif layer == "archive":
            if force_reload:
                self._load_jsonl_memories()
            return {
                "layer": "archive",
                "count": len(self._archive_memory),
                "loaded": True,
                "memory_ids": list(self._archive_memory.keys())
            }
        else:
            # Unknown layer
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
    
    def _load_jsonl_memories(self):
        """Load Application and Archive layer memories from JSONL files"""
        try:
            # Load Application layer memories
            app_memories = self._jsonl_dao.load_memories("application")
            self._app_memory.clear()
            for memory in app_memories:
                self._app_memory[memory["id"]] = memory
            
            # Load Archive layer memories
            archive_memories = self._jsonl_dao.load_memories("archive")
            self._archive_memory.clear()
            for memory in archive_memories:
                self._archive_memory[memory["id"]] = memory
                
        except Exception as e:
            print(f"Warning: Failed to load JSONL memories: {e}")
            self._app_memory = {}
            self._archive_memory = {}