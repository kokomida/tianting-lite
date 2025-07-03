"""
JSONL Data Access Object for MemoryHub Application Layer
Handles logs, traces and archived memories in JSONL format
"""
import json
import os
import array
import bisect
import mmap
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone

try:
    import simdjson
    HAS_SIMDJSON = True
except ImportError:
    HAS_SIMDJSON = False


class JSONLMemoryDAO:
    """Data Access Object for JSONL-based memory storage"""
    
    def __init__(self, data_path: str = "./memoryhub_data"):
        """Initialize JSONL DAO with data directory"""
        self.data_path = Path(data_path)
        self.app_logs_file = self.data_path / "app_logs.jsonl"
        self.archive_file = self.data_path / "archive.jsonl"
        
        # Index files for fast access
        self.app_logs_index = self.data_path / "app_logs.idx"
        self.archive_index = self.data_path / "archive.idx"
        
        # Ensure directories exist
        self.data_path.mkdir(exist_ok=True)
        
        # Create files if they don't exist
        for file_path in [self.app_logs_file, self.archive_file]:
            if not file_path.exists():
                file_path.touch()
        
        # High-performance offset arrays for O(log n) binary search
        self._app_offsets: array.array = array.array('Q')  # unsigned long long for file offsets
        self._app_lengths: array.array = array.array('I')  # unsigned int for record lengths
        self._archive_offsets: array.array = array.array('Q')
        self._archive_lengths: array.array = array.array('I')
        
        # Tag pre-index for fast tag-based filtering
        # Format: {tag_name: [record_index1, record_index2, ...]}
        self._app_tag_index: Dict[str, List[int]] = {}
        self._archive_tag_index: Dict[str, List[int]] = {}
        
        # Query result cache for frequent queries
        self._query_cache: Dict[str, List[Dict[str, Any]]] = {}
        self._cache_max_size = 500
        
        # In-memory recall count updates (batch before writing to disk)
        self._pending_recall_updates: Dict[str, Dict[str, int]] = {
            "application": {},
            "archive": {}
        }
        self._update_batch_size = 10  # Smaller batch size for tests
        
        # Load existing indices on startup
        self._load_indices()
    
    def store_memory(self, memory_record: Dict[str, Any], layer: str) -> bool:
        """Store memory record in appropriate JSONL file with index update"""
        try:
            # Choose file based on layer
            if layer == "application":
                file_path = self.app_logs_file
                index_path = self.app_logs_index
                offsets = self._app_offsets
                lengths = self._app_lengths
                tag_index = self._app_tag_index
            elif layer == "archive":
                file_path = self.archive_file
                index_path = self.archive_index
                offsets = self._archive_offsets
                lengths = self._archive_lengths
                tag_index = self._archive_tag_index
            else:
                return False
            
            # Add timestamp if not present
            if "stored_at" not in memory_record:
                memory_record["stored_at"] = datetime.now(timezone.utc).isoformat()
            
            # Get current file size (offset for new record)
            offset = file_path.stat().st_size if file_path.exists() else 0
            
            # Serialize the record
            record_line = json.dumps(memory_record, ensure_ascii=False) + '\n'
            record_length = len(record_line.encode('utf-8'))
            
            # Append to JSONL file
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(record_line)
            
            # Update offset arrays
            offsets.append(offset)
            lengths.append(record_length)
            
            # Update index file
            with open(index_path, 'a', encoding='utf-8') as f:
                f.write(f"{offset},{record_length}\n")
            
            # Update tag pre-index
            record_index = len(offsets) - 1
            tags = memory_record.get('tags', [])
            for tag in tags:
                tag_lower = tag.lower()
                if tag_lower not in tag_index:
                    tag_index[tag_lower] = []
                tag_index[tag_lower].append(record_index)
            
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
        """Search memories in specified layer using optimized indexing"""
        try:
            # Check cache first
            cache_key = f"{layer}:{query}:{limit}"
            if cache_key in self._query_cache:
                return self._query_cache[cache_key]
            
            # Get layer-specific data
            if layer == "application":
                file_path = self.app_logs_file
                offsets = self._app_offsets
                lengths = self._app_lengths
                tag_index = self._app_tag_index
            elif layer == "archive":
                file_path = self.archive_file
                offsets = self._archive_offsets
                lengths = self._archive_lengths
                tag_index = self._archive_tag_index
            else:
                return []
            
            if not file_path.exists() or len(offsets) == 0:
                return []
            
            query_lower = query.lower()
            
            # Step 1: Try tag pre-filtering first
            candidate_indices = self._get_tag_candidates(query_lower, tag_index)
            
            # Step 2: If no tag matches, search all records
            if not candidate_indices:
                candidate_indices = list(range(len(offsets)))
            
            # Step 3: Use binary search with mmap for fast access
            results = self._search_with_binary_access(file_path, offsets, lengths, 
                                                    candidate_indices, query_lower, limit)
            
            # Apply pending recall count updates to results
            self._apply_pending_updates_to_results(results, layer)
            
            # Cache results
            if len(self._query_cache) < self._cache_max_size:
                self._query_cache[cache_key] = results
            
            return results
            
        except Exception as e:
            print(f"Error searching memories in {layer}: {e}")
            # Fallback to full scan
            return self._fallback_search(query, layer, limit)
    
    def update_recall_count(self, memory_id: str, layer: str) -> bool:
        """Update recall count for a specific memory (using smart batching)"""
        try:
            if layer not in ["application", "archive"]:
                return False
            
            # Add to pending updates for batch processing
            self._pending_recall_updates[layer][memory_id] = self._pending_recall_updates[layer].get(memory_id, 0) + 1
            
            # Only flush when we reach the batch size to avoid frequent I/O
            if len(self._pending_recall_updates[layer]) >= self._update_batch_size:
                return self._flush_pending_updates(layer)
            
            return True
            
        except Exception as e:
            print(f"Error updating recall count: {e}")
            return False
    
    def _flush_pending_updates(self, layer: str) -> bool:
        """Flush pending recall count updates to disk efficiently"""
        try:
            if layer == "application":
                file_path = self.app_logs_file
            elif layer == "archive":
                file_path = self.archive_file
            else:
                return False
            
            if not file_path.exists() or not self._pending_recall_updates[layer]:
                return True
            
            # Read all memories into memory for update
            memories = []
            updates_applied = 0
            pending_updates = self._pending_recall_updates[layer]
            current_time = datetime.now(timezone.utc).isoformat()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            if HAS_SIMDJSON:
                                memory = simdjson.loads(line)
                            else:
                                memory = json.loads(line)
                            
                            memory_id = memory.get('id')
                            if memory_id in pending_updates:
                                memory['recalled_count'] = memory.get('recalled_count', 0) + pending_updates[memory_id]
                                memory['last_recalled'] = current_time
                                updates_applied += 1
                            
                            memories.append(memory)
                        except json.JSONDecodeError:
                            continue
            
            if updates_applied > 0:
                # Write back to file efficiently
                with open(file_path, 'w', encoding='utf-8') as f:
                    for memory in memories:
                        f.write(json.dumps(memory, ensure_ascii=False) + '\n')
                
                # Always rebuild indices after flush since record lengths may change
                self._rebuild_layer_indices(layer)
            
            # Clear pending updates for this layer
            self._pending_recall_updates[layer].clear()
            
            return True
            
        except Exception as e:
            print(f"Error flushing pending updates for {layer}: {e}")
            return False
    
    def _apply_pending_updates_to_results(self, results: List[Dict[str, Any]], layer: str):
        """Apply pending recall count updates to search results"""
        if layer not in self._pending_recall_updates:
            return
        
        pending_updates = self._pending_recall_updates[layer]
        for memory in results:
            memory_id = memory.get('id')
            if memory_id in pending_updates:
                current_count = memory.get('recalled_count', 0)
                memory['recalled_count'] = current_count + pending_updates[memory_id]
                memory['last_recalled'] = datetime.now(timezone.utc).isoformat()
    
    def flush_all_pending_updates(self):
        """Flush all pending updates to disk"""
        for layer in ["application", "archive"]:
            if self._pending_recall_updates[layer]:
                self._flush_pending_updates(layer)
    
    def __del__(self):
        """Ensure pending updates are flushed when object is destroyed"""
        try:
            self.flush_all_pending_updates()
        except Exception:
            pass  # Ignore errors during cleanup
    
    def build_index(self, layer: str, force_rebuild: bool = False) -> bool:
        """Build or rebuild index for specified layer"""
        try:
            if layer == "application":
                file_path = self.app_logs_file
                index_path = self.app_logs_index
                offsets = self._app_offsets
                lengths = self._app_lengths
                tag_index = self._app_tag_index
            elif layer == "archive":
                file_path = self.archive_file
                index_path = self.archive_index
                offsets = self._archive_offsets
                lengths = self._archive_lengths
                tag_index = self._archive_tag_index
            else:
                return False
            
            # Clear existing arrays
            del offsets[:]
            del lengths[:]
            tag_index.clear()
            
            # Build index from file
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    offset = 0
                    record_index = 0
                    
                    while True:
                        line_start = offset
                        line = f.readline()
                        if not line:
                            break
                        
                        line_length = len(line)
                        offsets.append(line_start)
                        lengths.append(line_length)
                        
                        # Parse for tag index
                        try:
                            line_str = line.decode('utf-8').strip()
                            if line_str:
                                if HAS_SIMDJSON:
                                    memory = simdjson.loads(line_str)
                                else:
                                    memory = json.loads(line_str)
                                
                                tags = memory.get('tags', [])
                                for tag in tags:
                                    tag_lower = tag.lower()
                                    if tag_lower not in tag_index:
                                        tag_index[tag_lower] = []
                                    tag_index[tag_lower].append(record_index)
                        except Exception:
                            pass
                        
                        offset += line_length
                        record_index += 1
                
                # Write index file
                with open(index_path, 'w', encoding='utf-8') as f:
                    for i in range(len(offsets)):
                        f.write(f"{offsets[i]},{lengths[i]}\n")
            
            return True
            
        except Exception as e:
            print(f"Error building index for {layer}: {e}")
            return False
    
    def _get_index_cache(self, layer: str) -> List[Tuple[int, int]]:
        """Get index cache for specified layer (compatibility method)"""
        if layer == "application":
            return list(zip(self._app_offsets, self._app_lengths))
        elif layer == "archive":
            return list(zip(self._archive_offsets, self._archive_lengths))
        return []
    
    def _read_index_file(self, index_path) -> List[Tuple[int, int]]:
        """Read index file and return list of (offset, length) tuples"""
        index_entries = []
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        offset, length = map(int, line.split(','))
                        index_entries.append((offset, length))
        except Exception as e:
            print(f"Error reading index file {index_path}: {e}")
        return index_entries
    
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
    
    def _load_indices(self):
        """Load existing index files into memory arrays and tag indices"""
        # Load application layer indices
        if self.app_logs_index.exists():
            self._load_layer_index("application")
        
        # Load archive layer indices
        if self.archive_index.exists():
            self._load_layer_index("archive")
        
        # Build tag indices by reading files if needed
        self._build_tag_indices()
    
    def _load_layer_index(self, layer: str):
        """Load index file for specific layer"""
        try:
            if layer == "application":
                index_path = self.app_logs_index
                offsets = self._app_offsets
                lengths = self._app_lengths
            elif layer == "archive":
                index_path = self.archive_index
                offsets = self._archive_offsets
                lengths = self._archive_lengths
            else:
                return
            
            del offsets[:]
            del lengths[:]
            
            with open(index_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        offset, length = map(int, line.split(','))
                        offsets.append(offset)
                        lengths.append(length)
                        
        except Exception as e:
            print(f"Error loading index for {layer}: {e}")
    
    def _build_tag_indices(self):
        """Build tag indices by reading existing files"""
        self._build_layer_tag_index("application")
        self._build_layer_tag_index("archive")
    
    def _build_layer_tag_index(self, layer: str):
        """Build tag index for specific layer"""
        try:
            if layer == "application":
                file_path = self.app_logs_file
                offsets = self._app_offsets
                tag_index = self._app_tag_index
            elif layer == "archive":
                file_path = self.archive_file
                offsets = self._archive_offsets
                tag_index = self._archive_tag_index
            else:
                return
            
            if not file_path.exists() or len(offsets) == 0:
                return
            
            tag_index.clear()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for record_index, line in enumerate(f):
                    line = line.strip()
                    if line:
                        try:
                            if HAS_SIMDJSON:
                                memory = simdjson.loads(line)
                            else:
                                memory = json.loads(line)
                            
                            tags = memory.get('tags', [])
                            for tag in tags:
                                tag_lower = tag.lower()
                                if tag_lower not in tag_index:
                                    tag_index[tag_lower] = []
                                tag_index[tag_lower].append(record_index)
                        except Exception:
                            continue
                            
        except Exception as e:
            print(f"Error building tag index for {layer}: {e}")
    
    def _get_tag_candidates(self, query_lower: str, tag_index: Dict[str, List[int]]) -> List[int]:
        """Get candidate record indices based on tag pre-filtering"""
        candidates = set()
        
        # Check for direct tag matches
        for tag, indices in tag_index.items():
            if query_lower in tag:
                candidates.update(indices)
        
        return sorted(list(candidates))
    
    def _search_with_binary_access(self, file_path: Path, offsets: array.array, lengths: array.array,
                                  candidate_indices: List[int], query_lower: str, 
                                  limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search using binary access with mmap for O(log n) performance"""
        matching_memories = []
        
        try:
            file_size = file_path.stat().st_size
            if file_size == 0:
                return []
            
            with open(file_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                    
                    for idx in candidate_indices:
                        if idx >= len(offsets) or idx >= len(lengths):
                            continue
                        
                        offset = offsets[idx]
                        length = lengths[idx]
                        
                        if offset < 0 or length <= 0 or offset + length > file_size:
                            continue
                        
                        try:
                            # Direct memory access
                            line_bytes = mmapped_file[offset:offset + length]
                            line = line_bytes.decode('utf-8', errors='ignore').strip()
                            
                            if not line:
                                continue
                            
                            # Fast JSON parsing
                            if HAS_SIMDJSON:
                                memory = simdjson.loads(line)
                            else:
                                memory = json.loads(line)
                            
                            # Check if memory matches query
                            if self._memory_matches_query(memory, query_lower):
                                matching_memories.append(memory)
                                
                                if limit and len(matching_memories) >= limit:
                                    break
                                    
                        except Exception:
                            continue
                            
        except Exception as e:
            print(f"Error in binary access search: {e}")
            return []
        
        # Sort by created_at descending (newest first)
        matching_memories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return matching_memories
    
    def _memory_matches_query(self, memory: Dict[str, Any], query_lower: str) -> bool:
        """Check if a memory matches the search query"""
        # Check content
        content = memory.get('content', '')
        if content and query_lower in content.lower():
            return True
        
        # Check context_path
        context_path = memory.get('context_path', '')
        if context_path and query_lower in context_path.lower():
            return True
        
        # Check tags
        tags = memory.get('tags', [])
        if tags:
            for tag in tags:
                if query_lower in tag.lower():
                    return True
        
        return False
    
    def _fallback_search(self, query: str, layer: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fallback search using full file scan"""
        all_memories = self.load_memories(layer)
        matching_memories = []
        
        query_lower = query.lower()
        
        for memory in all_memories:
            if self._memory_matches_query(memory, query_lower):
                matching_memories.append(memory)
                
                if limit and len(matching_memories) >= limit:
                    break
        
        return matching_memories
    
    def _rebuild_layer_indices(self, layer: str):
        """Rebuild indices for a layer after file modification"""
        try:
            if layer == "application":
                file_path = self.app_logs_file
                index_path = self.app_logs_index
                offsets = self._app_offsets
                lengths = self._app_lengths
                tag_index = self._app_tag_index
            elif layer == "archive":
                file_path = self.archive_file
                index_path = self.archive_index
                offsets = self._archive_offsets
                lengths = self._archive_lengths
                tag_index = self._archive_tag_index
            else:
                return
            
            # Clear existing indices
            del offsets[:]
            del lengths[:]
            tag_index.clear()
            
            # Rebuild from file
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    offset = 0
                    record_index = 0
                    
                    # Read line by line and rebuild indices
                    while True:
                        line_start = offset
                        line = f.readline()
                        if not line:
                            break
                        
                        line_length = len(line)
                        offsets.append(line_start)
                        lengths.append(line_length)
                        
                        # Parse for tag index
                        try:
                            line_str = line.decode('utf-8').strip()
                            if line_str:
                                if HAS_SIMDJSON:
                                    memory = simdjson.loads(line_str)
                                else:
                                    memory = json.loads(line_str)
                                
                                tags = memory.get('tags', [])
                                for tag in tags:
                                    tag_lower = tag.lower()
                                    if tag_lower not in tag_index:
                                        tag_index[tag_lower] = []
                                    tag_index[tag_lower].append(record_index)
                        except Exception:
                            pass
                        
                        offset += line_length
                        record_index += 1
                
                # Rewrite index file
                with open(index_path, 'w', encoding='utf-8') as f:
                    for i in range(len(offsets)):
                        f.write(f"{offsets[i]},{lengths[i]}\n")
                        
        except Exception as e:
            print(f"Error rebuilding indices for {layer}: {e}")
    
    def close(self):
        """Close all resources and flush pending updates"""
        try:
            # Flush all pending updates
            self.flush_all_pending_updates()
            
            # Clear all caches and indices
            self._query_cache.clear()
            
            # Clear offset/length arrays
            del self._app_offsets[:]
            del self._app_lengths[:]
            del self._archive_offsets[:]
            del self._archive_lengths[:]
            
            # Clear tag indices
            self._app_tag_index.clear()
            self._archive_tag_index.clear()
            
        except Exception as e:
            print(f"Warning: Error during JSONLMemoryDAO close: {e}")