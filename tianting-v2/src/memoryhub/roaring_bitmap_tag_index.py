"""
Roaring Bitmap Tag Index for MemoryHub

High-performance tag indexing using roaring bitmaps for efficient memory recall.
This module provides a compressed bitmap-based index for fast tag intersection operations.

Key Features:
- Compressed storage using roaring bitmaps
- Fast intersection/union operations
- Memory-efficient tag indexing
- Backward compatibility with existing tag systems

Performance Targets:
- 50-80% memory reduction vs dict-based indexing
- Sub-millisecond tag intersection operations
- Scalable to 100k+ memories with complex tag structures

Author: MemoryHub Team
Version: 0.3.0-alpha
"""

from typing import Set, Dict, List, Optional, Iterator, Tuple
from collections import defaultdict
import json
import logging

try:
    import pyroaring
    ROARING_AVAILABLE = True
except ImportError:
    ROARING_AVAILABLE = False
    import warnings
    warnings.warn("PyRoaring not available, falling back to dict-based indexing")

logger = logging.getLogger(__name__)


class RoaringBitmapTagIndex:
    """
    High-performance tag index using roaring bitmaps for memory-efficient storage.
    
    This class provides a compressed bitmap-based approach to tag indexing,
    significantly reducing memory usage while maintaining fast query performance.
    """
    
    def __init__(self, enable_compression: bool = True):
        """
        Initialize the roaring bitmap tag index.
        
        Args:
            enable_compression: Whether to enable bitmap compression (default: True)
        """
        self.enable_compression = enable_compression
        self._roaring_available = ROARING_AVAILABLE
        
        if self._roaring_available:
            # Tag -> RoaringBitmap mapping
            self._tag_to_bitmap: Dict[str, pyroaring.BitMap] = {}
            # Memory ID -> Set of tags mapping (for removal operations)
            self._memory_to_tags: Dict[int, Set[str]] = defaultdict(set)
        else:
            # Fallback to dict-based indexing
            self._tag_to_memory_ids: Dict[str, Set[int]] = defaultdict(set)
            self._memory_to_tags: Dict[int, Set[str]] = defaultdict(set)
        
        self._next_memory_id = 0
        self._memory_count = 0
        
        logger.info(f"RoaringBitmapTagIndex initialized (roaring: {self._roaring_available})")
    
    def add_memory(self, memory_id: int, tags: Set[str]) -> None:
        """
        Add a memory with its associated tags to the index.
        
        Args:
            memory_id: Unique identifier for the memory
            tags: Set of tags associated with the memory
        """
        if self._roaring_available:
            self._add_memory_roaring(memory_id, tags)
        else:
            self._add_memory_fallback(memory_id, tags)
        
        self._memory_count += 1
        logger.debug(f"Added memory {memory_id} with {len(tags)} tags")
    
    def _add_memory_roaring(self, memory_id: int, tags: Set[str]) -> None:
        """Add memory using roaring bitmap implementation."""
        for tag in tags:
            if tag not in self._tag_to_bitmap:
                self._tag_to_bitmap[tag] = pyroaring.BitMap()
            self._tag_to_bitmap[tag].add(memory_id)
        
        self._memory_to_tags[memory_id].update(tags)
    
    def _add_memory_fallback(self, memory_id: int, tags: Set[str]) -> None:
        """Add memory using fallback dict implementation."""
        for tag in tags:
            self._tag_to_memory_ids[tag].add(memory_id)
        
        self._memory_to_tags[memory_id].update(tags)
    
    def remove_memory(self, memory_id: int) -> bool:
        """
        Remove a memory from the index.
        
        Args:
            memory_id: Unique identifier for the memory to remove
            
        Returns:
            True if memory was found and removed, False otherwise
        """
        if memory_id not in self._memory_to_tags:
            return False
        
        tags = self._memory_to_tags[memory_id]
        
        if self._roaring_available:
            self._remove_memory_roaring(memory_id, tags)
        else:
            self._remove_memory_fallback(memory_id, tags)
        
        del self._memory_to_tags[memory_id]
        self._memory_count -= 1
        
        logger.debug(f"Removed memory {memory_id} with {len(tags)} tags")
        return True
    
    def _remove_memory_roaring(self, memory_id: int, tags: Set[str]) -> None:
        """Remove memory using roaring bitmap implementation."""
        for tag in tags:
            if tag in self._tag_to_bitmap:
                self._tag_to_bitmap[tag].discard(memory_id)
                # Clean up empty bitmaps
                if len(self._tag_to_bitmap[tag]) == 0:
                    del self._tag_to_bitmap[tag]
    
    def _remove_memory_fallback(self, memory_id: int, tags: Set[str]) -> None:
        """Remove memory using fallback dict implementation."""
        for tag in tags:
            if tag in self._tag_to_memory_ids:
                self._tag_to_memory_ids[tag].discard(memory_id)
                # Clean up empty sets
                if len(self._tag_to_memory_ids[tag]) == 0:
                    del self._tag_to_memory_ids[tag]
    
    def find_memories_by_tags(self, tags: Set[str], operation: str = "intersection") -> Set[int]:
        """
        Find memories that match the given tags using the specified operation.
        
        Args:
            tags: Set of tags to search for
            operation: Either "intersection" (AND) or "union" (OR)
            
        Returns:
            Set of memory IDs that match the criteria
        """
        if not tags:
            return set()
        
        if self._roaring_available:
            return self._find_memories_roaring(tags, operation)
        else:
            return self._find_memories_fallback(tags, operation)
    
    def _find_memories_roaring(self, tags: Set[str], operation: str) -> Set[int]:
        """Find memories using roaring bitmap implementation."""
        bitmaps = []
        
        for tag in tags:
            if tag in self._tag_to_bitmap:
                bitmaps.append(self._tag_to_bitmap[tag])
            elif operation == "intersection":
                # For intersection, if any tag doesn't exist, result is empty
                return set()
        
        if not bitmaps:
            return set()
        
        if operation == "intersection":
            result_bitmap = bitmaps[0]
            for bitmap in bitmaps[1:]:
                result_bitmap = result_bitmap & bitmap
        elif operation == "union":
            result_bitmap = bitmaps[0]
            for bitmap in bitmaps[1:]:
                result_bitmap = result_bitmap | bitmap
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return set(result_bitmap)
    
    def _find_memories_fallback(self, tags: Set[str], operation: str) -> Set[int]:
        """Find memories using fallback dict implementation."""
        memory_sets = []
        
        for tag in tags:
            if tag in self._tag_to_memory_ids:
                memory_sets.append(self._tag_to_memory_ids[tag])
            elif operation == "intersection":
                # For intersection, if any tag doesn't exist, result is empty
                return set()
        
        if not memory_sets:
            return set()
        
        if operation == "intersection":
            result = memory_sets[0]
            for memory_set in memory_sets[1:]:
                result = result & memory_set
        elif operation == "union":
            result = memory_sets[0]
            for memory_set in memory_sets[1:]:
                result = result | memory_set
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return result
    
    def get_tag_stats(self) -> Dict[str, int]:
        """
        Get statistics about tag usage.
        
        Returns:
            Dictionary mapping tags to their memory counts
        """
        if self._roaring_available:
            return {tag: len(bitmap) for tag, bitmap in self._tag_to_bitmap.items()}
        else:
            return {tag: len(memory_ids) for tag, memory_ids in self._tag_to_memory_ids.items()}
    
    def get_memory_efficiency(self) -> Dict[str, float]:
        """
        Get memory efficiency statistics.
        
        Returns:
            Dictionary with efficiency metrics
        """
        stats = {
            "total_memories": self._memory_count,
            "total_tags": len(self._tag_to_bitmap if self._roaring_available else self._tag_to_memory_ids),
            "average_tags_per_memory": 0.0,
            "compression_ratio": 1.0,
            "roaring_enabled": self._roaring_available
        }
        
        if self._memory_count > 0:
            total_tag_associations = sum(len(tags) for tags in self._memory_to_tags.values())
            stats["average_tags_per_memory"] = total_tag_associations / self._memory_count
        
        # TODO: Calculate actual compression ratio when we have baseline measurements
        
        return stats
    
    def clear(self) -> None:
        """Clear all data from the index."""
        if self._roaring_available:
            self._tag_to_bitmap.clear()
        else:
            self._tag_to_memory_ids.clear()
        
        self._memory_to_tags.clear()
        self._memory_count = 0
        
        logger.info("RoaringBitmapTagIndex cleared")
    
    def __len__(self) -> int:
        """Return the number of memories in the index."""
        return self._memory_count
    
    def __contains__(self, memory_id: int) -> bool:
        """Check if a memory ID exists in the index."""
        return memory_id in self._memory_to_tags


class RoaringBitmapTagIndexFactory:
    """Factory class for creating RoaringBitmapTagIndex instances."""
    
    @staticmethod
    def create_index(config: Optional[Dict] = None) -> RoaringBitmapTagIndex:
        """
        Create a new RoaringBitmapTagIndex instance.
        
        Args:
            config: Optional configuration dictionary
            
        Returns:
            New RoaringBitmapTagIndex instance
        """
        if config is None:
            config = {}
        
        enable_compression = config.get("enable_compression", True)
        
        return RoaringBitmapTagIndex(enable_compression=enable_compression)
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """
        Check if all required dependencies are available.
        
        Returns:
            Dictionary with dependency availability status
        """
        return {
            "pyroaring": ROARING_AVAILABLE,
            "fallback_available": True
        }


# Convenience functions for backward compatibility
def create_roaring_index(enable_compression: bool = True) -> RoaringBitmapTagIndex:
    """Create a new RoaringBitmapTagIndex instance."""
    return RoaringBitmapTagIndex(enable_compression=enable_compression)


def check_roaring_availability() -> bool:
    """Check if roaring bitmap functionality is available."""
    return ROARING_AVAILABLE


if __name__ == "__main__":
    # Simple test to verify the implementation
    index = RoaringBitmapTagIndex()
    
    # Add some test memories
    index.add_memory(1, {"python", "programming", "ai"})
    index.add_memory(2, {"python", "web", "django"})
    index.add_memory(3, {"ai", "machine-learning", "python"})
    
    # Test queries
    python_memories = index.find_memories_by_tags({"python"})
    ai_and_python = index.find_memories_by_tags({"ai", "python"}, "intersection")
    
    print(f"Python memories: {python_memories}")
    print(f"AI and Python memories: {ai_and_python}")
    print(f"Index stats: {index.get_tag_stats()}")
    print(f"Memory efficiency: {index.get_memory_efficiency()}")