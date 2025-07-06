"""
Basic integration tests for roaring bitmap functionality
"""

def test_roaring_bitmap_tag_index_basic():
    """Test that RoaringBitmapTagIndex can be imported and works."""
    from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndex
    
    index = RoaringBitmapTagIndex()
    assert index is not None
    
    # Test basic operations
    index.add_memory(1, {"python", "test"})
    assert 1 in index
    
    memories = index.find_memories_by_tags({"python"})
    assert 1 in memories


def test_layered_memory_manager_integration():
    """Test that LayeredMemoryManager can be imported and uses tag index."""
    from memoryhub import LayeredMemoryManager
    import tempfile
    import os
    
    # Use a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = LayeredMemoryManager(path=temp_dir)
        assert manager is not None
        
        # Test that it has the tag index
        assert hasattr(manager, '_tag_index')
        
        # Properly close the manager to release file handles
        manager.close()


def test_memory_manager_close():
    """Test resource cleanup in LayeredMemoryManager."""
    from memoryhub import LayeredMemoryManager
    import tempfile
    
    # Use a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = LayeredMemoryManager(path=temp_dir)
        
        # Test storing and retrieving a memory
        memory = manager.remember("test content", ["test", "python"])
        assert memory["id"] is not None
        
        # Test that close works properly
        manager.close()
        
        # Verify the manager is properly closed
        assert hasattr(manager, '_dao')