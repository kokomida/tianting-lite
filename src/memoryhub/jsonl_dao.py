"""
JSONL Data Access Object for MemoryHub Application Layer
Handles logs, traces and archived memories in JSONL format
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


class JSONLMemoryDAO:
    """Data Access Object for JSONL-based memory storage"""
    
    def __init__(self, data_path: str = "./memoryhub_data"):
        """Initialize JSONL DAO with data directory"""
        self.data_path = Path(data_path)
        self.app_logs_file = self.data_path / "app_logs.jsonl"
        self.archive_file = self.data_path / "archive.jsonl"
        
        # Ensure directories exist
        self.data_path.mkdir(exist_ok=True)
        
        # Create files if they don't exist
        for file_path in [self.app_logs_file, self.archive_file]:
            if not file_path.exists():
                file_path.touch()
    
    def store_memory(self, memory_record: Dict[str, Any], layer: str) -> bool:
        """Store memory record in appropriate JSONL file"""
        try:
            # Choose file based on layer
            if layer == "application":
                file_path = self.app_logs_file
            elif layer == "archive":
                file_path = self.archive_file
            else:
                return False
            
            # Add timestamp if not present
            if "stored_at" not in memory_record:
                memory_record["stored_at"] = datetime.now(timezone.utc).isoformat()
            
            # Append to JSONL file
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(memory_record, ensure_ascii=False) + '\n')
            
            return True
            
        except Exception as e:
            print(f"Error storing memory to {layer}: {e}")
            return False
    
    def load_memories(self, layer: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load memories from specified layer"""
        try:
            # Choose file based on layer
            if layer == "application":
                file_path = self.app_logs_file
            elif layer == "archive":
                file_path = self.archive_file
            else:
                return []
            
            if not file_path.exists():
                return []
            
            memories = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            memory = json.loads(line)
                            memories.append(memory)
                        except json.JSONDecodeError:
                            continue
            
            # Sort by created_at descending (newest first)
            memories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Apply limit if specified
            if limit:
                memories = memories[:limit]
            
            return memories
            
        except Exception as e:
            print(f"Error loading memories from {layer}: {e}")
            return []
    
    def search_memories(self, query: str, layer: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search memories in specified layer"""
        all_memories = self.load_memories(layer)
        matching_memories = []
        
        query_lower = query.lower()
        
        for memory in all_memories:
            # Search in content
            if query_lower in memory.get('content', '').lower():
                matching_memories.append(memory)
                continue
            
            # Search in tags
            tags = memory.get('tags', [])
            if any(query_lower in tag.lower() for tag in tags):
                matching_memories.append(memory)
                continue
            
            # Search in context_path
            if query_lower in memory.get('context_path', '').lower():
                matching_memories.append(memory)
                continue
        
        # Apply limit if specified
        if limit:
            matching_memories = matching_memories[:limit]
        
        return matching_memories
    
    def update_recall_count(self, memory_id: str, layer: str) -> bool:
        """Update recall count for a specific memory (reload file and rewrite)"""
        try:
            # Choose file based on layer
            if layer == "application":
                file_path = self.app_logs_file
            elif layer == "archive":
                file_path = self.archive_file
            else:
                return False
            
            if not file_path.exists():
                return False
            
            # Read all memories
            memories = []
            updated = False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            memory = json.loads(line)
                            if memory.get('id') == memory_id:
                                memory['recalled_count'] = memory.get('recalled_count', 0) + 1
                                memory['last_recalled'] = datetime.now(timezone.utc).isoformat()
                                updated = True
                            memories.append(memory)
                        except json.JSONDecodeError:
                            continue
            
            if updated:
                # Rewrite the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    for memory in memories:
                        f.write(json.dumps(memory, ensure_ascii=False) + '\n')
            
            return updated
            
        except Exception as e:
            print(f"Error updating recall count: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for JSONL layers"""
        stats = {
            "application_memory_count": 0,
            "archive_memory_count": 0,
            "total_recalls": 0,
            "files": {}
        }
        
        try:
            # Application layer stats
            app_memories = self.load_memories("application")
            stats["application_memory_count"] = len(app_memories)
            stats["files"]["app_logs"] = str(self.app_logs_file)
            
            # Archive layer stats
            archive_memories = self.load_memories("archive")
            stats["archive_memory_count"] = len(archive_memories)
            stats["files"]["archive"] = str(self.archive_file)
            
            # Count total recalls
            all_memories = app_memories + archive_memories
            stats["total_recalls"] = sum(
                memory.get('recalled_count', 0) for memory in all_memories
            )
            
        except Exception as e:
            print(f"Error getting JSONL stats: {e}")
        
        return stats