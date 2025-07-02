"""
Unit tests for LayeredMemoryManager basic functionality
"""
import pytest
import sys
import os

# Add src to path for imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from memoryhub.memory_manager import LayeredMemoryManager, MemoryLayer


class TestLayeredMemoryManagerBasic:
    """Test basic functionality of LayeredMemoryManager"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.memory_manager = LayeredMemoryManager()
    
    def test_init(self):
        """Test initialization"""
        assert self.memory_manager.path == "./memoryhub_data"
        assert len(self.memory_manager._session_memory) == 0
        assert self.memory_manager._memory_counter == 0
    
    def test_remember_basic(self):
        """Test basic remember functionality"""
        result = self.memory_manager.remember(
            content="Test memory content",
            tags=["test", "basic"],
            context_path="/test/path"
        )
        
        assert result["id"] == "mem_1"
        assert result["content"] == "Test memory content"
        assert result["tags"] == ["test", "basic"]
        assert result["context_path"] == "/test/path"
        assert result["layer"] == "session"
        assert "created_at" in result
        assert result["recalled_count"] == 0
    
    def test_remember_classification(self):
        """Test memory classification logic"""
        # Test CORE layer classification
        core_result = self.memory_manager.remember(
            content="Processing task_id ABC123",
            tags=["task"],
            context_path=""
        )
        # Note: In skeleton, all memories go to session but classification is tracked
        assert "task_id" in core_result["content"]
        
        # Test APPLICATION layer classification  
        app_result = self.memory_manager.remember(
            content="Log entry: system startup",
            tags=["system"],
            context_path=""
        )
        assert "log" in app_result["content"].lower()
        
        # Test ARCHIVE layer classification
        archive_result = self.memory_manager.remember(
            content="Old data",
            tags=["archive", "old"],
            context_path=""
        )
        assert "archive" in archive_result["tags"]
    
    def test_recall_basic(self):
        """Test basic recall functionality"""
        # Store some test memories
        self.memory_manager.remember("Python code example", ["python", "code"], "/code/example.py")
        self.memory_manager.remember("JavaScript function", ["js", "function"], "/js/utils.js")
        self.memory_manager.remember("Python unittest", ["python", "test"], "/tests/test_basic.py")
        
        # Test content search
        results = self.memory_manager.recall("Python")
        assert len(results) == 2
        assert all("python" in r["tags"] for r in results)
        
        # Test tag search
        results = self.memory_manager.recall("code")
        assert len(results) == 1
        assert "code" in results[0]["tags"]
        
        # Test context search
        results = self.memory_manager.recall("tests")
        assert len(results) == 1
        assert "/tests/" in results[0]["context_path"]
    
    def test_recall_limit(self):
        """Test recall limit functionality"""
        # Store multiple memories
        for i in range(5):
            self.memory_manager.remember(f"Test memory {i}", ["test"], f"/path/{i}")
        
        # Test limit
        results = self.memory_manager.recall("test", limit=3)
        assert len(results) == 3
    
    def test_recall_updates_stats(self):
        """Test that recall updates memory statistics"""
        self.memory_manager.remember("Test content", ["test"], "")
        
        initial_recall_count = self.memory_manager.stats()["memories_recalled"]
        self.memory_manager.recall("test")
        final_recall_count = self.memory_manager.stats()["memories_recalled"]
        
        assert final_recall_count > initial_recall_count
    
    def test_stats(self):
        """Test stats functionality"""
        initial_stats = self.memory_manager.stats()
        assert initial_stats["memories_stored"] == 0
        assert initial_stats["memories_recalled"] == 0
        assert initial_stats["session_memory_count"] == 0
        assert "created_at" in initial_stats
        
        # Add some memories
        self.memory_manager.remember("Test 1", ["test"], "")
        self.memory_manager.remember("Test 2", ["test"], "")
        
        updated_stats = self.memory_manager.stats()
        assert updated_stats["memories_stored"] == 2
        assert updated_stats["session_memory_count"] == 2
    
    def test_load_layer_session(self):
        """Test loading session layer"""
        # Add some memories
        self.memory_manager.remember("Test memory", ["test"], "")
        
        layer_info = self.memory_manager.load_layer("session")
        assert layer_info["layer"] == "session"
        assert layer_info["count"] == 1
        assert layer_info["loaded"] is True
        assert len(layer_info["memory_ids"]) == 1
    
    def test_load_layer_future(self):
        """Test loading future layers (not implemented)"""
        for layer in ["core", "app", "archive"]:
            layer_info = self.memory_manager.load_layer(layer)
            assert layer_info["layer"] == layer
            assert layer_info["count"] == 0
            assert layer_info["loaded"] is False
            assert layer_info["memory_ids"] == []
    
    def test_memory_classification_rules(self):
        """Test _classify_memory method directly"""
        mm = self.memory_manager
        
        # Test CORE classification
        assert mm._classify_memory("task_id: ABC123", []) == MemoryLayer.CORE
        assert mm._classify_memory("window_id: WIN001", []) == MemoryLayer.CORE
        
        # Test APPLICATION classification
        assert mm._classify_memory("log: system started", []) == MemoryLayer.APPLICATION
        assert mm._classify_memory("trace information", []) == MemoryLayer.APPLICATION
        
        # Test ARCHIVE classification
        assert mm._classify_memory("old data", ["archive"]) == MemoryLayer.ARCHIVE
        
        # Test SESSION classification (default)
        assert mm._classify_memory("regular content", ["normal"]) == MemoryLayer.SESSION


if __name__ == "__main__":
    pytest.main([__file__, "-v"])