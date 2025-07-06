"""
Tag Index Module for MemoryHub

This module provides a unified interface for tag indexing functionality,
currently wrapping the RoaringBitmapTagIndex implementation.
"""

from .roaring_bitmap_tag_index import RoaringBitmapTagIndex


# Provide a simple alias for backward compatibility
class TagIndex:
    """Simple wrapper around RoaringBitmapTagIndex for backward compatibility."""
    
    def __init__(self, enable_compression: bool = True):
        """Initialize the tag index."""
        self._index = RoaringBitmapTagIndex(enable_compression=enable_compression)
    
    def add_tags(self, memory_id: str, tags: list):
        """Add tags for a memory ID."""
        # Convert string memory_id to int hash for roaring bitmap
        memory_id_int = hash(memory_id) % (2**31)  # Keep it positive 32-bit
        self._index.add_memory(memory_id_int, set(tags))
    
    def remove_tags(self, memory_id: str):
        """Remove tags for a memory ID."""
        memory_id_int = hash(memory_id) % (2**31)
        return self._index.remove_memory(memory_id_int)
    
    def find_by_tags(self, tags: list, operation: str = "intersection"):
        """Find memories by tags."""
        return self._index.find_memories_by_tags(set(tags), operation)
    
    def get_stats(self):
        """Get tag statistics."""
        return self._index.get_tag_stats()
    
    def clear(self):
        """Clear all data."""
        self._index.clear()


# Export the main class for direct use
__all__ = ['RoaringBitmapTagIndex', 'TagIndex']