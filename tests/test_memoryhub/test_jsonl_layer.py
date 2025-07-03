"""
Unit tests for JSONL layer functionality in MemoryHub
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path

from memoryhub import LayeredMemoryManager
from memoryhub.memory_manager import MemoryLayer
from memoryhub.jsonl_dao import JSONLMemoryDAO


class TestJSONLLayer:
    """Test JSONL Application and Archive layer functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = LayeredMemoryManager(path=self.test_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_jsonl_file_creation(self):
        """Test that JSONL files are created properly"""
        app_logs_file = Path(self.test_dir) / "app_logs.jsonl"
        archive_file = Path(self.test_dir) / "archive.jsonl"
        
        assert app_logs_file.exists()
        assert archive_file.exists()
    
    def test_application_layer_persistence(self):
        """Test that Application layer memories persist to JSONL"""
        # Store a memory that should go to Application layer
        result = self.memory_manager.remember(
            content="Log: System startup completed successfully",
            tags=["system", "startup"],
            context_path="/logs/system.log"
        )
        
        assert result["layer"] == "application"
        
        # Verify it's in application memory
        stats = self.memory_manager.stats()
        assert stats["app_memory_count"] == 1
        
        # Create new instance to test persistence
        new_manager = LayeredMemoryManager(path=self.test_dir)
        new_stats = new_manager.stats()
        assert new_stats["app_memory_count"] == 1
        
        # Verify content is preserved
        results = new_manager.recall("startup")
        assert len(results) == 1
        assert results[0]["content"] == "Log: System startup completed successfully"
        assert "system" in results[0]["tags"]
    
    def test_archive_layer_persistence(self):
        """Test that Archive layer memories persist to JSONL"""
        # Store a memory that should go to Archive layer
        result = self.memory_manager.remember(
            content="Historical data from Q1 2024",
            tags=["archive", "quarterly", "data"],
            context_path="/archive/2024-q1.json"
        )
        
        assert result["layer"] == "archive"
        
        # Verify it's in archive memory
        stats = self.memory_manager.stats()
        assert stats["archive_memory_count"] == 1
        
        # Create new instance to test persistence
        new_manager = LayeredMemoryManager(path=self.test_dir)
        new_stats = new_manager.stats()
        assert new_stats["archive_memory_count"] == 1
        
        # Verify content is preserved
        results = new_manager.recall("quarterly")
        assert len(results) == 1
        assert results[0]["content"] == "Historical data from Q1 2024"
        assert "archive" in results[0]["tags"]
    
    def test_mixed_layer_recall_priority(self):
        """Test recall priority: Core > Application > Archive > Session"""
        # Store memories in different layers
        self.memory_manager.remember("task_id: CORE001", ["task"], "/core/task001")  # CORE
        self.memory_manager.remember("log: search query", ["log"], "/logs/search")   # APPLICATION
        self.memory_manager.remember("old search data", ["archive"], "/archive/old") # ARCHIVE
        self.memory_manager.remember("search session", ["temp"], "/session/temp")    # SESSION
        
        # Search for "search" - should return in priority order
        results = self.memory_manager.recall("search", limit=10)
        
        # Should find all 3 search-related memories (excluding core)
        assert len(results) >= 3
        
        # Core layer doesn't match "search", so first should be application layer
        # Then archive, then session
        layers = [result["layer"] for result in results]
        
        # Verify we have different layers represented
        assert "application" in layers
        assert "archive" in layers
        assert "session" in layers
    
    def test_jsonl_search_functionality(self):
        """Test JSONL layer search functionality"""
        # Store multiple memories in application layer
        self.memory_manager.remember("Log: User login failed", ["auth", "error"], "/logs/auth.log")
        self.memory_manager.remember("Log: Database connection established", ["db", "info"], "/logs/db.log")
        self.memory_manager.remember("Trace: API request processing", ["api", "trace"], "/logs/api.log")
        
        # Test content search
        results = self.memory_manager.recall("login")
        assert len(results) == 1
        assert "login failed" in results[0]["content"]
        
        # Test tag search
        results = self.memory_manager.recall("auth")
        assert len(results) == 1
        assert "auth" in results[0]["tags"]
        
        # Test context search
        results = self.memory_manager.recall("api.log")
        assert len(results) == 1
        assert "api.log" in results[0]["context_path"]
    
    def test_recall_count_persistence_jsonl(self):
        """Test that recall counts are persisted in JSONL files"""
        # Store an application memory
        self.memory_manager.remember("Log: Test recall count", ["test"], "/test/recall")
        
        # Recall it multiple times
        self.memory_manager.recall("recall")
        self.memory_manager.recall("recall")
        
        # Force flush pending updates to disk
        self.memory_manager.flush_pending_updates()
        
        # Create new instance and check recall count
        new_manager = LayeredMemoryManager(path=self.test_dir)
        results = new_manager.recall("recall")
        
        assert len(results) == 1
        # Should have recall count from previous instance + 1 from this recall
        assert results[0]["recalled_count"] >= 2
    
    def test_load_layer_jsonl(self):
        """Test loading JSONL layers specifically"""
        # Store memories in both layers
        self.memory_manager.remember("Log: Application test", ["app"], "/logs/app")
        self.memory_manager.remember("Archive: Old data", ["archive"], "/archive/old")
        
        # Test load_layer for application
        app_info = self.memory_manager.load_layer("application")
        assert app_info["layer"] == "application"
        assert app_info["count"] == 1
        assert app_info["loaded"] is True
        assert len(app_info["memory_ids"]) == 1
        
        # Test load_layer for archive
        archive_info = self.memory_manager.load_layer("archive")
        assert archive_info["layer"] == "archive"
        assert archive_info["count"] == 1
        assert archive_info["loaded"] is True
        assert len(archive_info["memory_ids"]) == 1
        
        # Test force reload
        app_info_reload = self.memory_manager.load_layer("app", force_reload=True)
        assert app_info_reload["count"] == 1
    
    def test_stats_with_jsonl_layers(self):
        """Test that stats include JSONL layer information"""
        # Store memories in different layers
        self.memory_manager.remember("task_id: STATS001", ["task"], "/task/stats")      # CORE
        self.memory_manager.remember("Log: Stats test", ["log"], "/logs/stats")         # APPLICATION
        self.memory_manager.remember("Archive: Stats old", ["archive"], "/archive/stats") # ARCHIVE
        self.memory_manager.remember("Session stats", ["temp"], "/session/stats")       # SESSION
        
        stats = self.memory_manager.stats()
        
        # Check layer counts
        assert stats["core_memory_count"] == 1
        assert stats["app_memory_count"] == 1
        assert stats["archive_memory_count"] == 1
        assert stats["session_memory_count"] == 1
        
        # Check JSONL stats are included
        assert "jsonl_stats" in stats
        assert "application_memory_count" in stats["jsonl_stats"]
        assert "archive_memory_count" in stats["jsonl_stats"]
        assert stats["jsonl_stats"]["application_memory_count"] == 1
        assert stats["jsonl_stats"]["archive_memory_count"] == 1


class TestJSONLMemoryDAO:
    """Test JSONLMemoryDAO directly"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_dir = tempfile.mkdtemp()
        self.dao = JSONLMemoryDAO(data_path=self.test_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_store_and_load_application_memory(self):
        """Test basic store and load operations for application layer"""
        memory_record = {
            "id": "app_001",
            "content": "Application log entry",
            "tags": ["app", "log"],
            "context_path": "/logs/app.log",
            "layer": "application",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        # Store memory
        success = self.dao.store_memory(memory_record, "application")
        assert success is True
        
        # Load memories
        memories = self.dao.load_memories("application")
        assert len(memories) == 1
        assert memories[0]["id"] == "app_001"
        assert memories[0]["content"] == "Application log entry"
        assert memories[0]["tags"] == ["app", "log"]
        assert "stored_at" in memories[0]  # Should be added automatically
    
    def test_store_and_load_archive_memory(self):
        """Test basic store and load operations for archive layer"""
        memory_record = {
            "id": "archive_001",
            "content": "Archived historical data",
            "tags": ["archive", "history"],
            "context_path": "/archive/history.json",
            "layer": "archive",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        # Store memory
        success = self.dao.store_memory(memory_record, "archive")
        assert success is True
        
        # Load memories
        memories = self.dao.load_memories("archive")
        assert len(memories) == 1
        assert memories[0]["id"] == "archive_001"
        assert memories[0]["content"] == "Archived historical data"
    
    def test_search_memories_jsonl(self):
        """Test search functionality in JSONL files"""
        # Store test memories
        memories = [
            {
                "id": "search_app_001",
                "content": "Python application log",
                "tags": ["python", "app"],
                "context_path": "/logs/python.log",
                "layer": "application",
                "created_at": "2025-07-02T10:00:00Z",
                "recalled_count": 0
            },
            {
                "id": "search_app_002", 
                "content": "JavaScript error handling",
                "tags": ["javascript", "error"],
                "context_path": "/logs/js.log",
                "layer": "application",
                "created_at": "2025-07-02T10:01:00Z",
                "recalled_count": 0
            }
        ]
        
        for memory in memories:
            self.dao.store_memory(memory, "application")
        
        # Test content search
        results = self.dao.search_memories("Python", "application")
        assert len(results) == 1
        assert "Python" in results[0]["content"]
        
        # Test tag search
        results = self.dao.search_memories("error", "application")
        assert len(results) == 1
        assert "error" in results[0]["tags"]
        
        # Test context search
        results = self.dao.search_memories("js.log", "application")
        assert len(results) == 1
        assert "js.log" in results[0]["context_path"]
    
    def test_update_recall_count_jsonl(self):
        """Test recall count updates in JSONL files"""
        memory_record = {
            "id": "recall_jsonl_001",
            "content": "Test JSONL recall count",
            "tags": ["test"],
            "context_path": "/test",
            "layer": "application",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        self.dao.store_memory(memory_record, "application")
        
        # Update recall count
        success = self.dao.update_recall_count("recall_jsonl_001", "application")
        assert success is True
        
        # Force flush to write updates to disk
        self.dao.flush_all_pending_updates()
        
        # Verify count was updated
        memories = self.dao.load_memories("application")
        assert len(memories) == 1
        assert memories[0]["recalled_count"] == 1
        assert "last_recalled" in memories[0]
    
    def test_get_stats_jsonl(self):
        """Test JSONL statistics"""
        # Store some test data
        app_memory = {
            "id": "stats_app_001",
            "content": "App stats test",
            "tags": ["stats"],
            "context_path": "/stats",
            "layer": "application",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 3
        }
        
        archive_memory = {
            "id": "stats_archive_001",
            "content": "Archive stats test",
            "tags": ["stats"],
            "context_path": "/archive",
            "layer": "archive",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 2
        }
        
        self.dao.store_memory(app_memory, "application")
        self.dao.store_memory(archive_memory, "archive")
        
        stats = self.dao.get_stats()
        assert "application_memory_count" in stats
        assert "archive_memory_count" in stats
        assert stats["application_memory_count"] == 1
        assert stats["archive_memory_count"] == 1
        assert stats["total_recalls"] == 5  # 3 + 2
        assert "files" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])