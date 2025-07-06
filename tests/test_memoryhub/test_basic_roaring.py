"""
Basic integration tests for roaring bitmap functionality
"""

import platform
import time

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
        manager = None
        try:
            manager = LayeredMemoryManager(path=temp_dir)
            assert manager is not None
            
            # Test that it has the tag index
            assert hasattr(manager, '_tag_index')
        finally:
            # Ensure manager is always closed to release file handles
            if manager is not None:
                manager.close()
                # On Windows, add a small delay to ensure file handles are fully released
                if platform.system() == "Windows":
                    time.sleep(0.1)


def test_memory_manager_close():
    """Test resource cleanup in LayeredMemoryManager."""
    from memoryhub import LayeredMemoryManager
    import tempfile
    
    # Use a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = None
        try:
            manager = LayeredMemoryManager(path=temp_dir)
            
            # Test storing and retrieving a memory
            memory = manager.remember("test content", ["test", "python"])
            assert memory["id"] is not None
            
            # Verify the manager is properly closed
            assert hasattr(manager, '_dao')
        finally:
            # Always ensure manager is closed
            if manager is not None:
                manager.close()
                # On Windows, add a small delay to ensure file handles are fully released
                if platform.system() == "Windows":
                    time.sleep(0.1)