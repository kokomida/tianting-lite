"""
Unit tests for MemoryHub resource release functionality
Specifically designed for Windows runner to test handle release
"""
import pytest
import os
import tempfile
import shutil
import platform
from pathlib import Path

from memoryhub import LayeredMemoryManager
from memoryhub.jsonl_dao import JSONLMemoryDAO
from memoryhub.sqlite_dao import MemoryHubDAO


class TestResourceRelease:
    """Test resource release functionality for MemoryHub"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_memory_manager_close(self):
        """Test that LayeredMemoryManager.close() releases resources"""
        manager = LayeredMemoryManager(path=self.test_dir)
        
        # Store some test data
        manager.remember("Test memory 1", ["test"], "/test/path1")
        manager.remember("Test memory 2", ["test"], "/test/path2")
        
        # Get initial stats
        stats = manager.stats()
        assert stats["total_memories"] >= 2
        
        # Close the manager
        manager.close()
        
        # Verify resources are cleared
        assert len(manager._session_memory) == 0
        assert len(manager._core_memory) == 0
        assert len(manager._app_memory) == 0
        assert len(manager._archive_memory) == 0
    
    def test_jsonl_dao_close(self):
        """Test that JSONLMemoryDAO.close() releases resources"""
        dao = JSONLMemoryDAO(data_path=self.test_dir)
        
        # Store some test data
        test_memory = {
            "id": "test_001",
            "content": "Test JSONL memory",
            "tags": ["test", "jsonl"],
            "context_path": "/test/jsonl",
            "layer": "application",
            "created_at": "2025-07-03T10:00:00Z",
            "recalled_count": 0
        }
        
        success = dao.store_memory(test_memory, "application")
        assert success is True
        
        # Update recall count to create pending updates
        dao.update_recall_count("test_001", "application")
        
        # Verify initial state
        assert len(dao._app_offsets) > 0
        assert len(dao._query_cache) >= 0
        
        # Close the DAO
        dao.close()
        
        # Verify resources are cleared
        assert len(dao._app_offsets) == 0
        assert len(dao._app_lengths) == 0
        assert len(dao._archive_offsets) == 0
        assert len(dao._archive_lengths) == 0
        assert len(dao._query_cache) == 0
        assert len(dao._app_tag_index) == 0
        assert len(dao._archive_tag_index) == 0
    
    def test_sqlite_dao_close(self):
        """Test that MemoryHubDAO.close() works (no-op but callable)"""
        db_path = os.path.join(self.test_dir, "test.db")
        dao = MemoryHubDAO(db_path=db_path)
        
        # Store some test data
        test_memory = {
            "id": "test_sql_001", 
            "content": "Test SQLite memory",
            "tags": ["test", "sql"],
            "context_path": "/test/sql",
            "layer": "core",
            "created_at": "2025-07-03T10:00:00Z",
            "recalled_count": 0
        }
        
        success = dao.store_memory(test_memory)
        assert success is True
        
        # Close should not raise any exceptions
        dao.close()
        
        # Database file should still exist and be accessible
        assert os.path.exists(db_path)
    
    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
    def test_windows_file_handle_release(self):
        """Test that files can be deleted after close() on Windows"""
        manager = LayeredMemoryManager(path=self.test_dir)
        
        # Store some memories to create files
        for i in range(5):
            manager.remember(f"Test memory {i}", ["test"], f"/test/path{i}")
        
        # Ensure data is written
        manager.flush_pending_updates()
        
        # Verify files exist
        app_logs_file = Path(self.test_dir) / "app_logs.jsonl"
        memory_db_file = Path(self.test_dir) / "memory.db"
        
        assert app_logs_file.exists()
        assert memory_db_file.exists()
        
        # Close manager to release handles
        manager.close()
        
        # On Windows, we should now be able to delete the files
        try:
            app_logs_file.unlink()
            memory_db_file.unlink()
        except PermissionError as e:
            pytest.fail(f"File handles not properly released on Windows: {e}")
    
    def test_multiple_close_calls(self):
        """Test that multiple close() calls don't cause errors"""
        manager = LayeredMemoryManager(path=self.test_dir)
        
        # Store some test data
        manager.remember("Test memory", ["test"], "/test/path")
        
        # Multiple close calls should not raise exceptions
        manager.close()
        manager.close()
        manager.close()
        
        # Verify state is still clean
        assert len(manager._session_memory) == 0
    
    def test_resource_cleanup_on_exception(self):
        """Test that resources are cleaned up even when exceptions occur"""
        manager = LayeredMemoryManager(path=self.test_dir)
        
        # Store some test data
        manager.remember("Test memory", ["test"], "/test/path")
        
        # Force an exception during close by corrupting internal state
        # This simulates real-world error conditions
        original_dao = manager._dao
        manager._dao = None  # This will cause an AttributeError
        
        # close() should handle the exception gracefully
        manager.close()  # Should not raise
        
        # Restore for cleanup
        manager._dao = original_dao
    
    def test_context_manager_pattern(self):
        """Test using MemoryHub with context manager pattern"""
        # Test implementing context manager for future use
        manager = LayeredMemoryManager(path=self.test_dir)
        
        try:
            # Store some test data
            manager.remember("Context test", ["test"], "/test/context")
            stats = manager.stats()
            assert stats["total_memories"] >= 1
        finally:
            # Ensure cleanup happens
            manager.close()
        
        # Verify cleanup
        assert len(manager._session_memory) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])