"""
Unit tests for MemoryHub statistics and performance tracking
"""
import pytest
import os
import tempfile
import shutil
import time

from memoryhub import LayeredMemoryManager
from memoryhub.memory_manager import MemoryLayer


class TestMemoryHubStats:
    """Test MemoryHub statistics functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = LayeredMemoryManager(path=self.test_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Close memory manager and database connections
        if hasattr(self, 'memory_manager'):
            self.memory_manager.close()
        
        # Clean up temporary directory with retry for Windows
        if os.path.exists(self.test_dir):
            for attempt in range(3):
                try:
                    shutil.rmtree(self.test_dir)
                    break
                except PermissionError:
                    if attempt < 2:  # Don't sleep on last attempt
                        time.sleep(0.1)
                    else:
                        # If still fails, just skip cleanup (CI will clean up temp files)
                        pass
    
    def test_initial_stats(self):
        """Test initial statistics state"""
        stats = self.memory_manager.stats()
        
        # Check basic counts
        assert stats["memories_stored"] == 0
        assert stats["memories_recalled"] == 0
        assert stats["total_memories"] == 0
        
        # Check layer counts
        assert stats["session_memory_count"] == 0
        assert stats["core_memory_count"] == 0
        assert stats["app_memory_count"] == 0
        assert stats["archive_memory_count"] == 0
        
        # Check performance stats
        assert "performance" in stats
        perf = stats["performance"]
        assert perf["avg_recall_latency_ms"] == 0.0
        assert perf["max_recall_latency_ms"] == 0.0
        assert perf["min_recall_latency_ms"] == 0.0
        assert perf["total_recall_time_ms"] == 0.0
        assert perf["recall_count"] == 0
        
        # Check nested stats
        assert "db_stats" in stats
        assert "jsonl_stats" in stats
    
    def test_memory_counting(self):
        """Test that memory counts are tracked correctly"""
        # Store memories in different layers
        self.memory_manager.remember("task_id: COUNT001", ["task"], "/task/count1")     # CORE
        self.memory_manager.remember("Log: Count test", ["log"], "/logs/count")          # APPLICATION
        self.memory_manager.remember("Archive count", ["archive"], "/archive/count")    # ARCHIVE
        self.memory_manager.remember("Session count", ["temp"], "/session/count")       # SESSION
        
        stats = self.memory_manager.stats()
        
        # Check individual layer counts
        assert stats["core_memory_count"] == 1
        assert stats["app_memory_count"] == 1
        assert stats["archive_memory_count"] == 1
        assert stats["session_memory_count"] == 1
        
        # Check total count
        assert stats["total_memories"] == 4
        assert stats["memories_stored"] == 4
    
    def test_recall_latency_tracking(self):
        """Test that recall latencies are tracked properly"""
        # Store some test memories
        self.memory_manager.remember("task_id: LATENCY001", ["latency"], "/task/lat1")
        self.memory_manager.remember("Log: Latency test", ["latency"], "/logs/lat")
        self.memory_manager.remember("Session latency", ["latency"], "/session/lat")
        
        # Perform some recalls
        results1 = self.memory_manager.recall("latency")
        results2 = self.memory_manager.recall("LATENCY001")
        results3 = self.memory_manager.recall("nonexistent")
        
        stats = self.memory_manager.stats()
        
        # Check that recalls were tracked
        assert stats["memories_recalled"] >= 3  # At least the results we found
        
        # Check performance metrics
        perf = stats["performance"]
        assert perf["recall_count"] == 3  # Number of recall operations
        assert perf["avg_recall_latency_ms"] >= 0.0
        assert perf["max_recall_latency_ms"] >= perf["avg_recall_latency_ms"]
        assert perf["min_recall_latency_ms"] <= perf["avg_recall_latency_ms"]
        assert perf["total_recall_time_ms"] >= 0.0
        
        # All latencies should be positive (even if very small)
        assert perf["avg_recall_latency_ms"] >= 0.0
        assert perf["max_recall_latency_ms"] >= 0.0
        
        # If we had any results, min should be positive too
        if stats["memories_recalled"] > 0:
            assert perf["min_recall_latency_ms"] >= 0.0
    
    def test_performance_consistency(self):
        """Test that performance metrics remain consistent"""
        # Store memories and perform multiple recalls
        for i in range(10):
            self.memory_manager.remember(f"test content {i}", ["test"], f"/test/{i}")
        
        # Perform multiple recalls to get meaningful stats
        for i in range(5):
            self.memory_manager.recall("test")
            self.memory_manager.recall(f"content {i}")
        
        stats = self.memory_manager.stats()
        perf = stats["performance"]
        
        # Check that all metrics are internally consistent
        assert perf["recall_count"] == 10  # 5 * 2 recalls
        assert perf["max_recall_latency_ms"] >= perf["avg_recall_latency_ms"]
        assert perf["avg_recall_latency_ms"] >= perf["min_recall_latency_ms"]
        assert perf["total_recall_time_ms"] >= 0.0
        
        # Average should be total divided by count
        expected_avg = perf["total_recall_time_ms"] / perf["recall_count"]
        assert abs(perf["avg_recall_latency_ms"] - expected_avg) < 1.0  # Relaxed for CI timing variance
    
    def test_layer_distribution_stats(self):
        """Test that layer distribution is calculated correctly"""
        # Store different numbers in each layer
        # Core: 3 memories
        for i in range(3):
            self.memory_manager.remember(f"task_id: DIST{i:03d}", ["dist"], f"/task/dist{i}")
        
        # Application: 2 memories
        for i in range(2):
            self.memory_manager.remember(f"Log: Distribution {i}", ["dist"], f"/logs/dist{i}")
        
        # Archive: 1 memory
        self.memory_manager.remember("Archive distribution", ["archive", "dist"], "/archive/dist")
        
        # Session: 4 memories
        for i in range(4):
            self.memory_manager.remember(f"Session dist {i}", ["dist"], f"/session/dist{i}")
        
        stats = self.memory_manager.stats()
        
        # Check distribution
        assert stats["core_memory_count"] == 3
        assert stats["app_memory_count"] == 2
        assert stats["archive_memory_count"] == 1
        assert stats["session_memory_count"] == 4
        assert stats["total_memories"] == 10
        
        # Also check in nested stats
        assert "db_stats" in stats
        assert stats["db_stats"]["core_memory_count"] == 3
        
        assert "jsonl_stats" in stats
        assert stats["jsonl_stats"]["application_memory_count"] == 2
        assert stats["jsonl_stats"]["archive_memory_count"] == 1
    
    def test_cross_instance_stats_persistence(self):
        """Test that stats persist correctly across instances"""
        # Store some memories
        self.memory_manager.remember("task_id: PERSIST001", ["persist"], "/task/p1")
        self.memory_manager.remember("Log: Persist test", ["persist"], "/logs/persist")
        
        # Perform some recalls
        self.memory_manager.recall("persist")
        self.memory_manager.recall("PERSIST001")
        
        # Create new instance (simulating restart)
        new_manager = LayeredMemoryManager(path=self.test_dir)
        
        # Perform recall on new instance
        new_manager.recall("persist")
        
        stats = new_manager.stats()
        
        # Check that persistent memories are counted
        assert stats["core_memory_count"] == 1  # Core memory should persist
        assert stats["app_memory_count"] == 1   # Application memory should persist
        assert stats["total_memories"] == 2     # Session memory won't persist
        
        # New instance should have its own performance stats
        perf = stats["performance"]
        assert perf["recall_count"] == 1  # Only the one recall on new instance
        assert perf["avg_recall_latency_ms"] >= 0.0
    
    def test_bulk_operations_stats(self):
        """Test stats with bulk operations"""
        # Store many memories at once using the regular test manager
        for i in range(20):  # Reduce size to speed up test
            content = f"Bulk test content {i:03d}"
            if i % 3 == 0:
                content = f"task_id: BULK{i:03d}"  # Force to core layer
            self.memory_manager.remember(content, ["bulk", "test"], f"/bulk/{i}")
        
        # Perform one recall and check that it's tracked
        initial_count = len(self.memory_manager._stats["recall_latencies"])
        self.memory_manager.recall("bulk")
        final_count = len(self.memory_manager._stats["recall_latencies"])
        
        stats = self.memory_manager.stats()
        
        # Check bulk stats
        assert stats["memories_stored"] == 20
        assert stats["total_memories"] == 20
        
        # Performance should be tracked (at least one more recall than initial)
        perf = stats["performance"]
        assert perf["recall_count"] == final_count
        assert perf["recall_count"] > initial_count  # Should have increased
        assert perf["avg_recall_latency_ms"] < 300.0  # Should be reasonable (relaxed for CI)
        
        # Check that we got results from the recall
        assert stats["memories_recalled"] > 0  # Should have found memories
        
        # All memories should be distributed across layers
        total_in_layers = (stats["session_memory_count"] + stats["core_memory_count"] + 
                          stats["app_memory_count"] + stats["archive_memory_count"])
        assert total_in_layers == 20


class TestStatsAPI:
    """Test the stats API specifically"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = LayeredMemoryManager(path=self.test_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Close memory manager and database connections
        if hasattr(self, 'memory_manager'):
            self.memory_manager.close()
        
        # Clean up temporary directory with retry for Windows
        if os.path.exists(self.test_dir):
            for attempt in range(3):
                try:
                    shutil.rmtree(self.test_dir)
                    break
                except PermissionError:
                    if attempt < 2:  # Don't sleep on last attempt
                        time.sleep(0.1)
                    else:
                        # If still fails, just skip cleanup (CI will clean up temp files)
                        pass
    
    def test_stats_api_structure(self):
        """Test that stats API returns expected structure"""
        stats = self.memory_manager.stats()
        
        # Required top-level fields
        required_fields = [
            "memories_stored", "memories_recalled", "total_memories",
            "session_memory_count", "core_memory_count", 
            "app_memory_count", "archive_memory_count",
            "performance", "db_stats", "jsonl_stats", 
            "layers_loaded", "created_at"
        ]
        
        for field in required_fields:
            assert field in stats, f"Missing required field: {field}"
        
        # Performance sub-structure
        perf_fields = [
            "avg_recall_latency_ms", "max_recall_latency_ms", 
            "min_recall_latency_ms", "total_recall_time_ms", "recall_count"
        ]
        
        for field in perf_fields:
            assert field in stats["performance"], f"Missing performance field: {field}"
    
    def test_stats_api_types(self):
        """Test that stats API returns correct data types"""
        # Add some data first
        self.memory_manager.remember("test content", ["test"], "/test")
        self.memory_manager.recall("test")
        
        stats = self.memory_manager.stats()
        
        # Check types
        assert isinstance(stats["memories_stored"], int)
        assert isinstance(stats["memories_recalled"], int)
        assert isinstance(stats["total_memories"], int)
        assert isinstance(stats["session_memory_count"], int)
        assert isinstance(stats["core_memory_count"], int)
        assert isinstance(stats["app_memory_count"], int)
        assert isinstance(stats["archive_memory_count"], int)
        
        # Performance metrics should be floats
        perf = stats["performance"]
        assert isinstance(perf["avg_recall_latency_ms"], float)
        assert isinstance(perf["max_recall_latency_ms"], float)
        assert isinstance(perf["min_recall_latency_ms"], float)
        assert isinstance(perf["total_recall_time_ms"], float)
        assert isinstance(perf["recall_count"], int)
        
        # Nested stats should be dicts
        assert isinstance(stats["db_stats"], dict)
        assert isinstance(stats["jsonl_stats"], dict)
        assert isinstance(stats["layers_loaded"], list)
        assert isinstance(stats["created_at"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])