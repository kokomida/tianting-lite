"""
Unit tests for SQLite persistence functionality in MemoryHub
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path

from memoryhub import LayeredMemoryManager
from memoryhub.memory_manager import MemoryLayer
from memoryhub.sqlite_dao import MemoryHubDAO


class TestSQLitePersistence:
    """Test SQLite persistence layer functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = LayeredMemoryManager(path=self.test_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_database_creation(self):
        """Test that SQLite database is created properly"""
        db_path = os.path.join(self.test_dir, "memory.db")
        assert os.path.exists(db_path)
    
    def test_core_memory_persistence(self):
        """Test that Core layer memories persist to SQLite"""
        # Store a memory that should go to Core layer
        result = self.memory_manager.remember(
            content="Processing task_id ABC123",
            tags=["task", "processing"],
            context_path="/tasks/ABC123"
        )
        
        assert result["layer"] == "core"
        
        # Verify it's in core memory
        stats = self.memory_manager.stats()
        assert stats["core_memory_count"] == 1
        
        # Create new instance to test persistence
        new_manager = LayeredMemoryManager(path=self.test_dir)
        new_stats = new_manager.stats()
        assert new_stats["core_memory_count"] == 1
        
        # Verify content is preserved
        results = new_manager.recall("task_id")
        assert len(results) == 1
        assert results[0]["content"] == "Processing task_id ABC123"
        assert "task" in results[0]["tags"]
    
    def test_session_memory_not_persisted(self):
        """Test that Session layer memories are not persisted"""
        # Store a memory that should go to Session layer
        result = self.memory_manager.remember(
            content="Regular session content",
            tags=["session", "temp"],
            context_path="/temp/session"
        )
        
        assert result["layer"] == "session"
        
        # Verify it's in session memory only
        stats = self.memory_manager.stats()
        assert stats["session_memory_count"] == 1
        assert stats["core_memory_count"] == 0
        
        # Create new instance - session memory should not persist
        new_manager = LayeredMemoryManager(path=self.test_dir)
        new_stats = new_manager.stats()
        assert new_stats["session_memory_count"] == 0
        assert new_stats["core_memory_count"] == 0
        
        # Should not find the session memory
        results = new_manager.recall("session")
        assert len(results) == 0
    
    def test_recall_across_instances(self):
        """Test recall functionality across different manager instances"""
        # Store multiple memories in different layers
        self.memory_manager.remember("task_id: CORE001", ["core"], "/core/task001")
        self.memory_manager.remember("log: application startup", ["app"], "/logs/startup")
        self.memory_manager.remember("session data", ["temp"], "/session/temp")
        
        # Create new instance and search
        new_manager = LayeredMemoryManager(path=self.test_dir)
        
        # Should find core memory
        core_results = new_manager.recall("CORE001")
        assert len(core_results) == 1
        assert "task_id: CORE001" in core_results[0]["content"]
        
        # Should not find session memory (not persisted)
        session_results = new_manager.recall("session data")
        assert len(session_results) == 0
    
    def test_recall_count_persistence(self):
        """Test that recall counts are persisted and updated"""
        # Store a core memory
        self.memory_manager.remember("task_id: RECALL_TEST", ["test"], "/test/recall")
        
        # Recall it multiple times
        self.memory_manager.recall("RECALL_TEST")
        self.memory_manager.recall("RECALL_TEST")
        
        # Create new instance and check recall count
        new_manager = LayeredMemoryManager(path=self.test_dir)
        results = new_manager.recall("RECALL_TEST")
        
        assert len(results) == 1
        # Should have recall count from previous instance + 1 from this recall
        assert results[0]["recalled_count"] >= 2
    
    def test_load_layer_core(self):
        """Test loading Core layer specifically"""
        # Store some core memories
        self.memory_manager.remember("task_id: LOAD001", ["test"], "/test/load1")
        self.memory_manager.remember("window_id: WIN001", ["test"], "/test/win1")
        
        # Test load_layer for core
        core_info = self.memory_manager.load_layer("core")
        assert core_info["layer"] == "core"
        assert core_info["count"] == 2
        assert core_info["loaded"] is True
        assert len(core_info["memory_ids"]) == 2
        
        # Test force reload
        core_info_reload = self.memory_manager.load_layer("core", force_reload=True)
        assert core_info_reload["count"] == 2
    
    def test_stats_with_database(self):
        """Test that stats include database information"""
        # Store memories in different layers
        self.memory_manager.remember("task_id: STATS001", ["test"], "/test/stats1")
        self.memory_manager.remember("session content", ["session"], "/session/stats")
        
        stats = self.memory_manager.stats()
        
        # Check basic counts
        assert stats["core_memory_count"] == 1
        assert stats["session_memory_count"] == 1
        
        # Check database stats are included
        assert "db_stats" in stats
        assert "core_memory_count" in stats["db_stats"]
        assert stats["db_stats"]["core_memory_count"] == 1


class TestMemoryHubDAO:
    """Test MemoryHubDAO directly"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_dir = tempfile.mkdtemp()
        self.dao = MemoryHubDAO(db_path=os.path.join(self.test_dir, "test.db"))
    
    def teardown_method(self):
        """Cleanup after each test method"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_store_and_load_memory(self):
        """Test basic store and load operations"""
        memory_record = {
            "id": "test_001",
            "content": "Test memory content",
            "tags": ["test", "dao"],
            "context_path": "/test/path",
            "layer": "core",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        # Store memory
        success = self.dao.store_memory(memory_record)
        assert success is True
        
        # Load memories
        memories = self.dao.load_memories("core")
        assert len(memories) == 1
        assert memories[0]["id"] == "test_001"
        assert memories[0]["content"] == "Test memory content"
        assert memories[0]["tags"] == ["test", "dao"]
    
    def test_search_memories(self):
        """Test search functionality"""
        # Store test memories
        memories = [
            {
                "id": "search_001",
                "content": "Python programming tutorial",
                "tags": ["python", "tutorial"],
                "context_path": "/tutorials/python.py",
                "layer": "core",
                "created_at": "2025-07-02T10:00:00Z",
                "recalled_count": 0
            },
            {
                "id": "search_002", 
                "content": "JavaScript function examples",
                "tags": ["javascript", "examples"],
                "context_path": "/examples/js.js",
                "layer": "core",
                "created_at": "2025-07-02T10:01:00Z",
                "recalled_count": 0
            }
        ]
        
        for memory in memories:
            self.dao.store_memory(memory)
        
        # Test content search
        results = self.dao.search_memories("Python", "core")
        assert len(results) == 1
        assert "Python" in results[0]["content"]
        
        # Test tag search
        results = self.dao.search_memories("tutorial", "core")
        assert len(results) == 1
        assert "tutorial" in results[0]["tags"]
        
        # Test context search
        results = self.dao.search_memories("examples", "core")
        assert len(results) == 1
        assert "examples" in results[0]["context_path"]
    
    def test_update_recall_count(self):
        """Test recall count updates"""
        memory_record = {
            "id": "recall_001",
            "content": "Test recall count",
            "tags": ["test"],
            "context_path": "/test",
            "layer": "core", 
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        self.dao.store_memory(memory_record)
        
        # Update recall count
        success = self.dao.update_recall_count("recall_001")
        assert success is True
        
        # Verify count was updated
        memories = self.dao.load_memories("core")
        assert len(memories) == 1
        assert memories[0]["recalled_count"] == 1
    
    def test_get_stats(self):
        """Test database statistics"""
        # Store some test data
        memory_record = {
            "id": "stats_001",
            "content": "Stats test",
            "tags": ["stats"],
            "context_path": "/stats",
            "layer": "core",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 5
        }
        
        self.dao.store_memory(memory_record)
        
        stats = self.dao.get_stats()
        assert "core_memory_count" in stats
        assert stats["core_memory_count"] == 1
        assert stats["total_recalls"] == 5
        assert "tables" in stats
        assert "tasks" in stats["tables"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])