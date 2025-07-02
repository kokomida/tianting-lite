#!/usr/bin/env python3
"""
Simple test runner for MemoryHub tests
"""
import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Import and run tests
from memoryhub.memory_manager import LayeredMemoryManager, MemoryLayer

def test_basic_functionality():
    """Test basic MemoryHub functionality"""
    print("Testing LayeredMemoryManager basic functionality...")
    
    # Initialize
    mm = LayeredMemoryManager()
    print("✅ Initialization successful")
    
    # Test remember
    result = mm.remember("Test content", ["test"], "/test/path")
    assert result["id"] == "mem_1"
    assert result["content"] == "Test content"
    print("✅ Remember functionality works")
    
    # Test recall
    results = mm.recall("test")
    assert len(results) == 1
    assert results[0]["content"] == "Test content"
    print("✅ Recall functionality works")
    
    # Test stats
    stats = mm.stats()
    assert stats["memories_stored"] == 1
    assert stats["session_memory_count"] == 1
    print("✅ Stats functionality works")
    
    # Test classification
    assert mm._classify_memory("task_id ABC", []) == MemoryLayer.CORE
    assert mm._classify_memory("log entry", []) == MemoryLayer.APPLICATION
    assert mm._classify_memory("old data", ["archive"]) == MemoryLayer.ARCHIVE
    assert mm._classify_memory("normal content", []) == MemoryLayer.SESSION
    print("✅ Memory classification works")
    
    print("\n🎉 All tests passed!")

if __name__ == "__main__":
    test_basic_functionality()