"""
Basic tests for RoaringBitmapTagIndex functionality
"""

import pytest
import sys


def test_roaring_bitmap_tag_index_basic():
    """Test basic functionality of RoaringBitmapTagIndex."""
    from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndex
    
    # Test initialization
    index = RoaringBitmapTagIndex()
    assert index is not None
    
    # Test basic operations
    index.add_memory(1, ["tag1", "tag2"])
    index.add_memory(2, ["tag2", "tag3"]) 
    index.add_memory(3, ["tag1", "tag3"])
    
    # Test retrieval
    result = index.find_memories_by_tags(["tag1"])
    assert 1 in result and 3 in result
    
    result = index.find_memories_by_tags(["tag2"])
    assert 1 in result and 2 in result
    
    # Test intersection
    result = index.find_memories_by_tags(["tag1", "tag2"])
    assert 1 in result
    assert len(result) == 1
    
    # Test removal
    index.remove_memory(1)
    result = index.find_memories_by_tags(["tag1"])
    assert 3 in result and 1 not in result


def test_layered_memory_manager_integration():
    """Test that LayeredMemoryManager can be imported and uses tag index."""
    from memoryhub import LayeredMemoryManager
    
    # Test that we can create an instance
    manager = LayeredMemoryManager(
        db_path=":memory:",
        app_logs_path=None,
        archive_logs_path=None
    )
    assert manager is not None
    
    # Test that it has the tag index
    assert hasattr(manager, '_tag_index')
    assert hasattr(manager, 'recall_by_tags')
    
    # Clean up
    try:
        manager.close()
    except:
        pass


def test_memory_manager_close():
    """Test resource cleanup in LayeredMemoryManager."""
    from memoryhub import LayeredMemoryManager
    
    manager = LayeredMemoryManager(
        db_path=":memory:",
        app_logs_path=None, 
        archive_logs_path=None
    )
    
    # Should not raise an exception
    manager.close()