"""
Tests for RoaringBitmapTagIndex

This module contains comprehensive tests for the roaring bitmap tag index implementation,
including both roaring bitmap and fallback modes with proper mocking.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os
from typing import Set

# Add src to path to import memoryhub modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


# Mock pyroaring.BitMap class for testing
class MockBitMap:
    """Mock implementation of pyroaring.BitMap for testing"""
    
    def __init__(self):
        self._data = set()
    
    def add(self, item):
        self._data.add(item)
    
    def discard(self, item):
        self._data.discard(item)
    
    def __len__(self):
        return len(self._data)
    
    def __contains__(self, item):
        return item in self._data
    
    def __iter__(self):
        return iter(self._data)
    
    def __and__(self, other):
        """Intersection operation"""
        result = MockBitMap()
        result._data = self._data & other._data
        return result
    
    def __or__(self, other):
        """Union operation"""
        result = MockBitMap()
        result._data = self._data | other._data
        return result


@pytest.fixture(scope="module", params=[True, False])
def roaring_available(request):
    """Parametrized fixture to test both roaring and fallback modes."""
    return request.param


@pytest.fixture
def mock_pyroaring(roaring_available):
    """Mock pyroaring based on availability parameter."""
    if roaring_available:
        # Create mock pyroaring module
        mock_pyroaring = MagicMock()
        mock_pyroaring.BitMap = MockBitMap
        
        with patch.dict('sys.modules', {'pyroaring': mock_pyroaring}):
            yield True
    else:
        # Simulate ImportError for pyroaring
        with patch.dict('sys.modules', {'pyroaring': None}):
            original_import = __import__
            
            def mock_import(name, *args, **kwargs):
                if name == 'pyroaring':
                    raise ImportError("No module named 'pyroaring'")
                return original_import(name, *args, **kwargs)
            
            with patch('builtins.__import__', side_effect=mock_import):
                yield False


@pytest.fixture
def tag_index(mock_pyroaring):
    """Create a fresh RoaringBitmapTagIndex instance for each test."""
    # Import here to ensure the mock is in place
    from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndex
    return RoaringBitmapTagIndex()


class TestRoaringBitmapTagIndex:
    """Test suite for RoaringBitmapTagIndex with both roaring and fallback modes."""
    
    def test_initialization(self, tag_index, roaring_available):
        """Test that the index initializes correctly in both modes."""
        assert len(tag_index) == 0
        assert tag_index._memory_count == 0
        assert tag_index._roaring_available == roaring_available
        
        if roaring_available:
            assert hasattr(tag_index, '_tag_to_bitmap')
            assert isinstance(tag_index._tag_to_bitmap, dict)
        else:
            assert hasattr(tag_index, '_tag_to_memory_ids')
            assert isinstance(tag_index._tag_to_memory_ids, dict)
    
    def test_add_single_memory(self, tag_index, roaring_available):
        """Test adding a single memory with tags."""
        memory_id = 1
        tags = {"python", "programming", "ai"}
        
        tag_index.add_memory(memory_id, tags)
        
        assert len(tag_index) == 1
        assert memory_id in tag_index
        assert tag_index._memory_to_tags[memory_id] == tags
        
        # Verify internal structure based on mode
        if roaring_available:
            assert len(tag_index._tag_to_bitmap) == 3
            for tag in tags:
                assert tag in tag_index._tag_to_bitmap
                assert memory_id in tag_index._tag_to_bitmap[tag]
        else:
            assert len(tag_index._tag_to_memory_ids) == 3
            for tag in tags:
                assert tag in tag_index._tag_to_memory_ids
                assert memory_id in tag_index._tag_to_memory_ids[tag]
    
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
        
        # Check tag statistics
        stats = tag_index.get_tag_stats()
        expected_stats = {
            "python": 3,  # memories 1, 2, 3
            "programming": 2,  # memories 1, 4
            "ai": 2,  # memories 1, 3
            "web": 1,  # memory 2
            "django": 1,  # memory 2
            "machine-learning": 1,  # memory 3
            "java": 1,  # memory 4
            "spring": 1  # memory 4
        }
        assert stats == expected_stats
    
    def test_remove_memory(self, tag_index, roaring_available):
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
        
        # Check that tags are properly cleaned up
        stats = tag_index.get_tag_stats()
        expected_stats = {"python": 1, "web": 1}  # Only memory 2 remains
        assert stats == expected_stats
        
        # Verify internal cleanup based on mode
        if roaring_available:
            assert "ai" not in tag_index._tag_to_bitmap  # Should be cleaned up
            assert "python" in tag_index._tag_to_bitmap
            assert 1 not in tag_index._tag_to_bitmap["python"]
        else:
            assert "ai" not in tag_index._tag_to_memory_ids  # Should be cleaned up
            assert "python" in tag_index._tag_to_memory_ids
            assert 1 not in tag_index._tag_to_memory_ids["python"]
        
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
        java_memories = tag_index.find_memories_by_tags({"java"})
        
        assert python_memories == {1, 2}
        assert web_memories == {2, 3}
        assert java_memories == {3}
    
    def test_find_memories_by_tags_intersection(self, tag_index):
        """Test finding memories by tag intersection (AND operation)."""
        tag_index.add_memory(1, {"python", "ai", "machine-learning"})
        tag_index.add_memory(2, {"python", "web", "django"})
        tag_index.add_memory(3, {"ai", "machine-learning", "tensorflow"})
        tag_index.add_memory(4, {"python", "ai", "nlp"})
        
        # Find memories that have both python AND ai
        result = tag_index.find_memories_by_tags({"python", "ai"}, "intersection")
        assert result == {1, 4}
        
        # Find memories that have both ai AND machine-learning
        result = tag_index.find_memories_by_tags({"ai", "machine-learning"}, "intersection")
        assert result == {1, 3}
        
        # Find memories with three tags
        result = tag_index.find_memories_by_tags({"python", "ai", "machine-learning"}, "intersection")
        assert result == {1}
    
    def test_find_memories_by_tags_union(self, tag_index):
        """Test finding memories by tag union (OR operation)."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        tag_index.add_memory(3, {"java", "web"})
        tag_index.add_memory(4, {"go", "backend"})
        
        # Find memories that have either python OR java
        result = tag_index.find_memories_by_tags({"python", "java"}, "union")
        assert result == {1, 2, 3}
        
        # Find memories that have either ai OR backend
        result = tag_index.find_memories_by_tags({"ai", "backend"}, "union")
        assert result == {1, 4}
        
        # Find memories with all different tags
        result = tag_index.find_memories_by_tags({"python", "java", "go"}, "union")
        assert result == {1, 2, 3, 4}
    
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
        
        result = tag_index.find_memories_by_tags({"python", "nonexistent"}, "intersection")
        assert result == set()
    
    def test_get_memory_efficiency(self, tag_index, roaring_available):
        """Test getting memory efficiency statistics."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        
        efficiency = tag_index.get_memory_efficiency()
        
        assert efficiency["total_memories"] == 2
        assert efficiency["total_tags"] == 3  # python, ai, web
        assert efficiency["average_tags_per_memory"] == 2.0  # (2 + 2) / 2
        assert efficiency["roaring_enabled"] == roaring_available
        assert "compression_ratio" in efficiency
    
    def test_clear_index(self, tag_index, roaring_available):
        """Test clearing the index."""
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"java", "web"})
        
        assert len(tag_index) == 2
        
        tag_index.clear()
        
        assert len(tag_index) == 0
        assert tag_index._memory_count == 0
        assert len(tag_index._memory_to_tags) == 0
        
        # Verify internal structures are cleared based on mode
        if roaring_available:
            assert len(tag_index._tag_to_bitmap) == 0
        else:
            assert len(tag_index._tag_to_memory_ids) == 0
    
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
        
        # Very long tags
        long_tag = "a" * 1000
        tag_index.add_memory(4, {long_tag})
        result = tag_index.find_memories_by_tags({long_tag})
        assert result == {4}


class TestRoaringBitmapBehaviorSpecific:
    """Tests specific to roaring bitmap behavior when available."""
    
    @pytest.mark.parametrize("roaring_available", [True], indirect=True)
    def test_bitmap_operations(self, tag_index, mock_pyroaring):
        """Test that bitmap operations work correctly."""
        # Add memories with overlapping tags
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        tag_index.add_memory(3, {"ai", "ml"})
        
        # Test that internal bitmaps are MockBitMap instances
        assert isinstance(tag_index._tag_to_bitmap["python"], MockBitMap)
        assert isinstance(tag_index._tag_to_bitmap["ai"], MockBitMap)
        
        # Test bitmap intersection
        python_bitmap = tag_index._tag_to_bitmap["python"]
        ai_bitmap = tag_index._tag_to_bitmap["ai"]
        intersection = python_bitmap & ai_bitmap
        
        assert isinstance(intersection, MockBitMap)
        assert 1 in intersection  # Only memory 1 has both python and ai
        assert 2 not in intersection
        assert 3 not in intersection
        
        # Test bitmap union
        union = python_bitmap | ai_bitmap
        assert 1 in union
        assert 2 in union
        assert 3 in union


class TestFallbackBehaviorSpecific:
    """Tests specific to fallback behavior when pyroaring is not available."""
    
    @pytest.mark.parametrize("roaring_available", [False], indirect=True)
    def test_fallback_set_operations(self, tag_index, mock_pyroaring):
        """Test that set operations work correctly in fallback mode."""
        # Add memories with overlapping tags
        tag_index.add_memory(1, {"python", "ai"})
        tag_index.add_memory(2, {"python", "web"})
        tag_index.add_memory(3, {"ai", "ml"})
        
        # Test that internal structures are regular sets
        assert isinstance(tag_index._tag_to_memory_ids["python"], set)
        assert isinstance(tag_index._tag_to_memory_ids["ai"], set)
        
        # Test set intersection
        python_set = tag_index._tag_to_memory_ids["python"]
        ai_set = tag_index._tag_to_memory_ids["ai"]
        intersection = python_set & ai_set
        
        assert intersection == {1}  # Only memory 1 has both python and ai
        
        # Test set union
        union = python_set | ai_set
        assert union == {1, 2, 3}


class TestRoaringBitmapTagIndexFactory:
    """Test suite for RoaringBitmapTagIndexFactory."""
    
    def test_create_index_default(self, mock_pyroaring):
        """Test creating index with default configuration."""
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndexFactory
        
        index = RoaringBitmapTagIndexFactory.create_index()
        
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndex
        assert isinstance(index, RoaringBitmapTagIndex)
        assert index.enable_compression is True
    
    def test_create_index_with_config(self, mock_pyroaring):
        """Test creating index with custom configuration."""
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndexFactory
        
        config = {"enable_compression": False}
        index = RoaringBitmapTagIndexFactory.create_index(config)
        
        assert index.enable_compression is False
    
    def test_check_dependencies(self, mock_pyroaring, roaring_available):
        """Test dependency checking."""
        from memoryhub.roaring_bitmap_tag_index import RoaringBitmapTagIndexFactory
        
        deps = RoaringBitmapTagIndexFactory.check_dependencies()
        
        assert "pyroaring" in deps
        assert "fallback_available" in deps
        assert deps["fallback_available"] is True
        assert deps["pyroaring"] == roaring_available


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    def test_create_roaring_index(self, mock_pyroaring):
        """Test the create_roaring_index convenience function."""
        from memoryhub.roaring_bitmap_tag_index import create_roaring_index
        
        index = create_roaring_index()
        assert index.enable_compression is True
        
        index = create_roaring_index(enable_compression=False)
        assert index.enable_compression is False
    
    def test_check_roaring_availability(self, mock_pyroaring, roaring_available):
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
        
        # Test memory efficiency stats
        efficiency = tag_index.get_memory_efficiency()
        assert efficiency["total_memories"] == 100
        assert efficiency["average_tags_per_memory"] == 3.0
    
    def test_memory_cleanup_after_removal(self, tag_index, roaring_available):
        """Test that memory is properly cleaned up after removal."""
        # Add memories
        for i in range(10):
            tag_index.add_memory(i, {f"tag_{i}"})
        
        # Remove all memories
        for i in range(10):
            tag_index.remove_memory(i)
        
        assert len(tag_index) == 0
        
        # Check that internal structures are cleaned up
        if roaring_available:
            assert len(tag_index._tag_to_bitmap) == 0
        else:
            assert len(tag_index._tag_to_memory_ids) == 0
        
        assert len(tag_index._memory_to_tags) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])