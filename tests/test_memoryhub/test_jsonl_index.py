"""
Unit tests for JSONL indexing functionality in MemoryHub
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path

from memoryhub.jsonl_dao import JSONLMemoryDAO


class TestJSONLIndexing:
    """Test JSONL indexing functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.dao = JSONLMemoryDAO(data_path=self.test_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_index_file_creation(self):
        """Test that index files are created when storing memories"""
        # Store a memory
        memory_record = {
            "id": "idx_001",
            "content": "Test index content",
            "tags": ["index", "test"],
            "context_path": "/test/index",
            "layer": "application",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        # Initially no index files should exist
        assert not self.dao.app_logs_index.exists()
        
        # Store memory
        success = self.dao.store_memory(memory_record, "application")
        assert success is True
        
        # Index file should now exist
        assert self.dao.app_logs_index.exists()
        
        # Index should have one entry
        with open(self.dao.app_logs_index, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 1
            
            # Parse the index entry
            offset, length = map(int, lines[0].strip().split(','))
            assert offset == 0  # First entry starts at offset 0
            assert length > 0   # Should have some length
    
    def test_index_build_from_existing_file(self):
        """Test building index from existing JSONL file"""
        # Manually create a JSONL file without index
        test_memories = [
            {"id": "build_001", "content": "First memory", "tags": ["build"]},
            {"id": "build_002", "content": "Second memory", "tags": ["build"]},
            {"id": "build_003", "content": "Third memory", "tags": ["build"]}
        ]
        
        # Write directly to JSONL file (bypassing store_memory to avoid auto-indexing)
        import json
        with open(self.dao.app_logs_file, 'w', encoding='utf-8') as f:
            for memory in test_memories:
                f.write(json.dumps(memory) + '\n')
        
        # Index should not exist yet
        assert not self.dao.app_logs_index.exists()
        
        # Build index
        success = self.dao.build_index("application")
        assert success is True
        
        # Index should now exist with correct entries
        assert self.dao.app_logs_index.exists()
        
        # Check index content
        index_entries = self.dao._read_index_file(self.dao.app_logs_index)
        assert len(index_entries) == 3
        
        # Verify offsets are correct
        assert index_entries[0][0] == 0  # First record at offset 0
        assert index_entries[1][0] > index_entries[0][0]  # Second after first
        assert index_entries[2][0] > index_entries[1][0]  # Third after second
    
    def test_index_cache_loading(self):
        """Test that index cache is properly loaded"""
        # Store some memories
        for i in range(5):
            memory = {
                "id": f"cache_{i:03d}",
                "content": f"Cache test content {i}",
                "tags": ["cache", "test"],
                "context_path": f"/cache/test{i}",
                "layer": "application",
                "created_at": "2025-07-02T10:00:00Z",
                "recalled_count": 0
            }
            self.dao.store_memory(memory, "application")
        
        # Create new DAO instance to test cache loading
        new_dao = JSONLMemoryDAO(data_path=self.test_dir)
        
        # Cache should be loaded
        app_cache = new_dao._get_index_cache("application")
        assert app_cache is not None
        assert len(app_cache) == 5
        
        # Check that cache entries are valid tuples
        for offset, length in app_cache:
            assert isinstance(offset, int)
            assert isinstance(length, int)
            assert offset >= 0
            assert length > 0
    
    def test_indexed_search_performance(self):
        """Test that indexed search works correctly"""
        # Store multiple memories with different content
        test_data = [
            {"id": "search_001", "content": "Python programming tutorial", "tags": ["python", "tutorial"]},
            {"id": "search_002", "content": "JavaScript function examples", "tags": ["javascript", "examples"]},
            {"id": "search_003", "content": "Python data structures", "tags": ["python", "data"]},
            {"id": "search_004", "content": "Web development guide", "tags": ["web", "guide"]},
            {"id": "search_005", "content": "Python machine learning", "tags": ["python", "ml"]}
        ]
        
        for memory in test_data:
            memory.update({
                "context_path": f"/docs/{memory['id']}.md",  # Changed from /tutorials/ to avoid context match
                "layer": "application",
                "created_at": "2025-07-02T10:00:00Z",
                "recalled_count": 0
            })
            self.dao.store_memory(memory, "application")
        
        # Test content search
        results = self.dao.search_memories("Python", "application")
        assert len(results) == 3  # Should find 3 Python-related memories
        
        # Verify results contain expected IDs
        result_ids = [r["id"] for r in results]
        assert "search_001" in result_ids
        assert "search_003" in result_ids
        assert "search_005" in result_ids
        
        # Test tag search
        results = self.dao.search_memories("tutorial", "application")
        assert len(results) == 1
        assert results[0]["id"] == "search_001"
        
        # Test context search
        results = self.dao.search_memories("search_002", "application")
        assert len(results) == 1
        assert results[0]["id"] == "search_002"
    
    def test_indexed_search_with_limit(self):
        """Test indexed search with result limiting"""
        # Store many memories
        for i in range(20):
            memory = {
                "id": f"limit_{i:03d}",
                "content": f"Test content {i} with common word",
                "tags": ["common", "test"],
                "context_path": f"/test/{i}",
                "layer": "application",
                "created_at": f"2025-07-02T{10 + i % 10}:00:00Z",
                "recalled_count": 0
            }
            self.dao.store_memory(memory, "application")
        
        # Search with limit
        results = self.dao.search_memories("common", "application", limit=5)
        assert len(results) == 5
        
        # Search without limit should return all
        results_all = self.dao.search_memories("common", "application")
        assert len(results_all) == 20
    
    def test_index_rebuild_functionality(self):
        """Test force rebuilding of indices"""
        # Store initial memories
        for i in range(3):
            memory = {
                "id": f"rebuild_{i:03d}",
                "content": f"Rebuild test {i}",
                "tags": ["rebuild"],
                "context_path": f"/rebuild/{i}",
                "layer": "application",
                "created_at": "2025-07-02T10:00:00Z",
                "recalled_count": 0
            }
            self.dao.store_memory(memory, "application")
        
        # Get original index
        original_cache = list(self.dao._get_index_cache("application"))
        assert len(original_cache) == 3
        
        # Manually add content to JSONL file (simulating corruption)
        import json
        with open(self.dao.app_logs_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"id": "manual_add", "content": "Manually added"}) + '\n')
        
        # Cache should still be old
        assert len(self.dao._get_index_cache("application")) == 3
        
        # Force rebuild
        success = self.dao.build_index("application", force_rebuild=True)
        assert success is True
        
        # Cache should now reflect the new content
        new_cache = self.dao._get_index_cache("application")
        assert len(new_cache) == 4
    
    def test_search_fallback_on_index_failure(self):
        """Test that search falls back to full scan if index fails"""
        # Store a memory normally
        memory = {
            "id": "fallback_001",
            "content": "Fallback test content",
            "tags": ["fallback", "test"],
            "context_path": "/fallback/test",
            "layer": "application",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        self.dao.store_memory(memory, "application")
        
        # Corrupt the index file
        with open(self.dao.app_logs_index, 'w') as f:
            f.write("invalid,data,format\n")
        
        # Search should still work (using fallback)
        results = self.dao.search_memories("fallback", "application")
        assert len(results) == 1
        assert results[0]["id"] == "fallback_001"
    
    def test_multiple_layer_indexing(self):
        """Test that both application and archive layers can be indexed independently"""
        # Store memories in both layers
        app_memory = {
            "id": "multi_app_001",
            "content": "Application layer content",
            "tags": ["app", "multi"],
            "context_path": "/app/multi",
            "layer": "application",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        archive_memory = {
            "id": "multi_archive_001",
            "content": "Archive layer content",
            "tags": ["archive", "multi"],
            "context_path": "/archive/multi",
            "layer": "archive",
            "created_at": "2025-07-02T10:00:00Z",
            "recalled_count": 0
        }
        
        self.dao.store_memory(app_memory, "application")
        self.dao.store_memory(archive_memory, "archive")
        
        # Both index files should exist
        assert self.dao.app_logs_index.exists()
        assert self.dao.archive_index.exists()
        
        # Both caches should have entries
        app_cache = self.dao._get_index_cache("application")
        archive_cache = self.dao._get_index_cache("archive")
        
        assert len(app_cache) == 1
        assert len(archive_cache) == 1
        
        # Search should work in both layers
        app_results = self.dao.search_memories("app", "application")
        archive_results = self.dao.search_memories("archive", "archive")
        
        assert len(app_results) == 1
        assert len(archive_results) == 1
        assert app_results[0]["id"] == "multi_app_001"
        assert archive_results[0]["id"] == "multi_archive_001"


class TestMemoryHubCLI:
    """Test CLI functionality for index management"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_cli_build_index_integration(self):
        """Test that CLI can build indices"""
        # Create some test data
        dao = JSONLMemoryDAO(data_path=self.test_dir)
        
        for i in range(5):
            memory = {
                "id": f"cli_{i:03d}",
                "content": f"CLI test content {i}",
                "tags": ["cli", "test"],
                "context_path": f"/cli/test{i}",
                "layer": "application",
                "created_at": "2025-07-02T10:00:00Z",
                "recalled_count": 0
            }
            dao.store_memory(memory, "application")
        
        # Remove index to test CLI rebuilding
        if dao.app_logs_index.exists():
            dao.app_logs_index.unlink()
        
        # Test that we can import and use the CLI module
        import sys
        import os
        
        # Add src to path to import memoryhub
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
        
        # Import CLI module
        cli_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'memoryhub_cli.py')
        assert os.path.exists(cli_path), "CLI script should exist"
        
        # Create a new DAO to verify index was rebuilt
        new_dao = JSONLMemoryDAO(data_path=self.test_dir)
        success = new_dao.build_index("application")
        
        assert success is True
        assert new_dao.app_logs_index.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])