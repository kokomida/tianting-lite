"""
Tests for RoaringBitmapTagIndex

This module contains comprehensive tests for the roaring bitmap tag index implementation,
including both roaring bitmap and fallback modes.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from collections import defaultdict

# Test both with and without pyroaring available
@pytest.fixture(scope="module", params=[True, False])
def roaring_available(request):
    """Parametrized fixture to test both roaring and fallback modes."""
    return request.param


@pytest.fixture
def mock_roaring_import(roaring_available):
    """Mock pyroaring import based on availability parameter."""
    if roaring_available:
        # Mock pyroaring.BitMap
        mock_bitmap = MagicMock()
        mock_bitmap.__len__ = lambda self: len(self._data)
        mock_bitmap.__contains__ = lambda self, item: item in self._data
        mock_bitmap.__iter__ = lambda self: iter(self._data)
        mock_bitmap.add = lambda self, item: self._data.add(item)
        mock_bitmap.discard = lambda self, item: self._data.discard(item)
        mock_bitmap.__and__ = lambda self, other: self._intersection(other)
        mock_bitmap.__or__ = lambda self, other: self._union(other)
        
        def create_bitmap():
            bitmap = MagicMock()
            bitmap._data = set()
            bitmap.__len__ = lambda: len(bitmap._data)
            bitmap.__contains__ = lambda item: item in bitmap._data
            bitmap.__iter__ = lambda: iter(bitmap._data)
            bitmap.add = lambda item: bitmap._data.add(item)
            bitmap.discard = lambda item: bitmap._data.discard(item)
            bitmap.__and__ = lambda other: create_intersection(bitmap, other)
            bitmap.__or__ = lambda other: create_union(bitmap, other)
            return bitmap
        
        def create_intersection(bitmap1, bitmap2):
            result = create_bitmap()
            result._data = bitmap1._data & bitmap2._data
            return result
        
        def create_union(bitmap1, bitmap2):
            result = create_bitmap()
            result._data = bitmap1._data | bitmap2._data
            return result
        
        mock_module = MagicMock()
        mock_module.BitMap = create_bitmap
        
        with patch.dict('sys.modules', {'pyroaring': mock_module}):
            yield True
    else:
        # Remove pyroaring from sys.modules if it exists
        if 'pyroaring' in sys.modules:
            del sys.modules['pyroaring']
        
        with patch.dict('sys.modules', {'pyroaring': None}):
            with patch('builtins.__import__', side_effect=lambda name, *args: None if name == 'pyroaring' else __import__(name, *args)):
                yield False


@pytest.fixture
def tag_index(mock_roaring_import):
    """Create a fresh RoaringBitmapTagIndex instance for each test."""
    # Import here to ensure the mock is in place
    from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndex
    return RoaringBitmapTagIndex()


class TestRoaringBitmapTagIndex:
    """Test suite for RoaringBitmapTagIndex."""
    
    def test_initialization(self, tag_index, roaring_available):
        """Test that the index initializes correctly in both modes."""
        assert len(tag_index) == 0
        assert tag_index._memory_count == 0
        assert tag_index._roaring_available == roaring_available
    
    def test_add_single_memory(self, tag_index):
        """Test adding a single memory with tags."""
        memory_id = 1
        tags = {"python", "programming", "ai"}
        
        tag_index.add_memory(memory_id, tags)
        
        assert len(tag_index) == 1
        assert memory_id in tag_index
        assert tag_index._memory_to_tags[memory_id] == tags
    
    def test_add_multiple_memories(self, tag_index):
        """Test adding multiple memories with overlapping tags."""
        memories = [
            (1, {"python", "programming", "ai"}),
            (2, {"python", "web", "django"}),
            (3, {"ai", "machine-learning", "python"}),
            (4, {"java", "programming", "spring"})
        ]
        
        for memory_id, tags in memories:
            tag_index.add_memory(memory_id, tags)
        
        assert len(tag_index) == 4
        
        # Check that all memories are indexed
        for memory_id, tags in memories:
            assert memory_id in tag_index
            assert tag_index._memory_to_tags[memory_id] == tags
    
    def test_remove_memory(self, tag_index):
        """Test removing a memory from the index."""
        # Add memories
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        
        # Remove one memory
        result = tag_index.remove_memory(1)
        
        assert result is True
        assert len(tag_index) == 1
        assert 1 not in tag_index
        assert 2 in tag_index
        
        # Try to remove non-existent memory
        result = tag_index.remove_memory(99)
        assert result is False
        assert len(tag_index) == 1
    
    def test_find_memories_by_single_tag(self, tag_index):
        """Test finding memories by a single tag."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        tag_index.add_memory(3, {"java", "web"})
        
        python_memories = tag_index.find_memories_by_tags({"python"})
        web_memories = tag_index.find_memories_by_tags({"web"})
        
        assert python_memories == {1, 2}
        assert web_memories == {2, 3}
    
    def test_find_memories_by_tags_intersection(self, tag_index):
        """Test finding memories by tag intersection (AND operation)."""
        tag_index.add_memory(1, {"python", "ai", "machine-learning"})
        tag_index.add_memory(2, {"python", "web", "django"})
        tag_index.add_memory(3, {"ai", "machine-learning", "tensorflow"})
        
        # Find memories that have both python AND ai
        result = tag_index.find_memories_by_tags({"python", "ai"}, "intersection")
        assert result == {1}
        
        # Find memories that have both ai AND machine-learning
        result = tag_index.find_memories_by_tags({"ai", "machine-learning"}, "intersection")
        assert result == {1, 3}
    
    def test_find_memories_by_tags_union(self, tag_index):
        """Test finding memories by tag union (OR operation)."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        tag_index.add_memory(3, {"java", "web"})
        
        # Find memories that have either python OR java
        result = tag_index.find_memories_by_tags({"python", "java"}, "union")
        assert result == {1, 2, 3}
        
        # Find memories that have either ai OR web
        result = tag_index.find_memories_by_tags({"ai", "web"}, "union")
        assert result == {1, 2, 3}
    
    def test_find_memories_empty_tags(self, tag_index):
        """Test finding memories with empty tag set."""
        tag_index.add_memory(1, {"python"})
        
        result = tag_index.find_memories_by_tags(set())
        assert result == set()
    
    def test_find_memories_nonexistent_tags(self, tag_index):
        """Test finding memories with non-existent tags."""
        tag_index.add_memory(1, {"python"})
        
        result = tag_index.find_memories_by_tags({"nonexistent"})
        assert result == set()
    
    def test_get_tag_stats(self, tag_index):
        """Test getting tag statistics."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        tag_index.add_memory(3, {"java", "web"})
        
        stats = tag_index.get_tag_stats()
        
        expected = {
            "python": 2,
            "ai": 1,
            "web": 2,
            "java": 1
        }
        
        assert stats == expected
    
    def test_get_memory_efficiency(self, tag_index):
        """Test getting memory efficiency statistics."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        
        efficiency = tag_index.get_memory_efficiency()
        
        assert efficiency["total_memories"] == 2
        assert efficiency["total_tags"] == 3  # python, ai, web
        assert efficiency["average_tags_per_memory"] == 2.0  # (2 + 2) / 2
        assert "roaring_enabled" in efficiency
        assert "compression_ratio" in efficiency
    
    def test_clear_index(self, tag_index):
        """Test clearing the index."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"java", "web"})
        
        assert len(tag_index) == 2
        
        tag_index.clear()
        
        assert len(tag_index) == 0
        assert tag_index._memory_count == 0
        assert len(tag_index._memory_to_tags) == 0
    
    def test_invalid_operation(self, tag_index):
        """Test using invalid operation parameter."""
        tag_index.add_memory(1, {"python"})
        
        with pytest.raises(ValueError, match="Unsupported operation"):
            tag_index.find_memories_by_tags({"python"}, "invalid_operation")
    
    def test_edge_cases(self, tag_index):
        """Test various edge cases."""
        # Empty tags
        tag_index.add_memory(1, set())
        assert len(tag_index) == 1
        assert 1 in tag_index
        
        # Single character tags
        tag_index.add_memory(2, {"a", "b"})
        result = tag_index.find_memories_by_tags({"a"})
        assert result == {2}
        
        # Unicode tags
        tag_index.add_memory(3, {"αβγ", "测试"})
        result = tag_index.find_memories_by_tags({"αβγ"})
        assert result == {3}


class TestRoaringBitmapTagIndexFactory:
    """Test suite for RoaringBitmapTagIndexFactory."""
    
    def test_create_index_default(self, mock_roaring_import):
        """Test creating index with default configuration."""
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndexFactory
        
        index = RoaringBitmapTagIndexFactory.create_index()
        
        assert isinstance(index, type(index))
        assert index.enable_compression is True
    
    def test_create_index_with_config(self, mock_roaring_import):
        """Test creating index with custom configuration."""
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndexFactory
        
        config = {"enable_compression": False}
        index = RoaringBitmapTagIndexFactory.create_index(config)
        
        assert index.enable_compression is False
    
    def test_check_dependencies(self, mock_roaring_import, roaring_available):
        """Test dependency checking."""
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndexFactory
        
        deps = RoaringBitmapTagIndexFactory.check_dependencies()
        
        assert "pyroaring" in deps
        assert "fallback_available" in deps
        assert deps["fallback_available"] is True
        assert deps["pyroaring"] == roaring_available


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    def test_create_roaring_index(self, mock_roaring_import):
        """Test the create_roaring_index convenience function."""
        from memoryhub.roaring_bitmap_tag_index import create_roaring_index
        
        index = create_roaring_index()
        assert index.enable_compression is True
        
        index = create_roaring_index(enable_compression=False)
        assert index.enable_compression is False
    
    def test_check_roaring_availability(self, mock_roaring_import, roaring_available):
        """Test the check_roaring_availability convenience function."""
        from memoryhub.roaring_bitmap_tag_index import check_roaring_availability
        
        result = check_roaring_availability()
        assert result == roaring_available


class TestPerformanceConsiderations:
    """Test suite focusing on performance-related aspects."""
    
    def test_large_dataset_simulation(self, tag_index):
        """Test behavior with a larger dataset to ensure scalability."""
        # Add many memories with overlapping tags
        for i in range(100):
            tags = {f"tag_{i % 10}", f"category_{i % 5}", f"type_{i % 3}"}
            tag_index.add_memory(i, tags)
        
        assert len(tag_index) == 100
        
        # Test intersection query performance
        result = tag_index.find_memories_by_tags({"tag_0", "category_0"}, "intersection")
        assert len(result) > 0
        
        # Test union query performance
        result = tag_index.find_memories_by_tags({"tag_0", "tag_1"}, "union")
        assert len(result) > 0
    
    def test_memory_cleanup_after_removal(self, tag_index):
        """Test that memory is properly cleaned up after removal."""
        # Add memories
        for i in range(10):
            tag_index.add_memory(i, {f"tag_{i}"})
        
        # Remove all memories
        for i in range(10):
            tag_index.remove_memory(i)
        
        assert len(tag_index) == 0
        
        # Check that internal structures are cleaned up
        if tag_index._roaring_available:
            assert len(tag_index._tag_to_bitmap) == 0
        else:
            assert len(tag_index._tag_to_memory_ids) == 0
        
        assert len(tag_index._memory_to_tags) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])