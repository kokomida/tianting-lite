#!/usr/bin/env python3
"""
MemoryHub Performance Benchmark Script
Evaluates recall latency on 10k memories across different layers
"""
import sys
import os
import time
import tempfile
import shutil
from pathlib import Path

# Add src to path to import memoryhub
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from memoryhub import LayeredMemoryManager


def generate_test_data(count: int):
    """Generate test memory data for benchmarking"""
    test_data = []
    
    for i in range(count):
        # Distribute across different layers based on content patterns
        if i % 4 == 0:  # Core layer - 25%
            content = f"task_id: BENCH_{i:06d} - Core business logic"
            tags = ["task", "core", "benchmark"]
            context = f"/tasks/bench_{i:06d}.json"
        elif i % 4 == 1:  # Application layer - 25%
            content = f"Log: Processing request {i:06d} - Application trace"
            tags = ["log", "app", "benchmark"]
            context = f"/logs/app_{i:06d}.log"
        elif i % 4 == 2:  # Archive layer - 25%
            content = f"Historical data entry {i:06d} - Archived record"
            tags = ["archive", "historical", "benchmark"]
            context = f"/archive/data_{i:06d}.json"
        else:  # Session layer - 25%
            content = f"Temporary session data {i:06d} - Session state"
            tags = ["session", "temp", "benchmark"]
            context = f"/session/temp_{i:06d}.tmp"
        
        test_data.append({
            "content": content,
            "tags": tags,
            "context_path": context
        })
    
    return test_data


def benchmark_memory_operations(memory_count: int = 10000, recall_queries: int = 1000):
    """
    Benchmark MemoryHub operations
    
    Args:
        memory_count: Number of memories to store
        recall_queries: Number of recall operations to perform
        
    Returns:
        Dict containing benchmark results
    """
    # Create temporary directory for test
    test_dir = tempfile.mkdtemp(prefix="memoryhub_benchmark_")
    
    try:
        print(f"🔥 Starting MemoryHub Benchmark")
        print(f"📊 Test data: {memory_count:,} memories, {recall_queries:,} recalls")
        print(f"📁 Test directory: {test_dir}")
        print()
        
        # Generate test data
        print("🏗️  Generating test data...")
        test_data = generate_test_data(memory_count)
        
        # Initialize MemoryHub with context manager
        with LayeredMemoryManager(path=test_dir) as memory_manager:
            # Phase 1: Store memories
            print("💾 Phase 1: Storing memories...")
            store_start = time.time()
            
            for i, data in enumerate(test_data):
                memory_manager.remember(
                    content=data["content"],
                    tags=data["tags"],
                    context_path=data["context_path"]
                )
                
                if (i + 1) % 1000 == 0:
                    print(f"    Stored {i + 1:,} memories...")
            
            store_end = time.time()
            store_time = store_end - store_start
            
            print(f"✅ Storage completed in {store_time:.2f}s")
            print(f"   Rate: {memory_count / store_time:.0f} memories/sec")
            print()
            
            # Phase 2: Recall benchmark
            print("🔍 Phase 2: Recall benchmark...")
            
            # Test queries across different terms
            test_queries = [
                "BENCH_000001", "task", "log", "archive", "session", 
                "Processing", "Historical", "Temporary", "Core", "Application",
                "000100", "001000", "002000", "005000", "009999"
            ]
            
            recall_times = []
            total_results = 0
            
            recall_start = time.time()
            
            for i in range(recall_queries):
                query = test_queries[i % len(test_queries)]
                
                start_time = time.time()
                results = memory_manager.recall(query, limit=10)
                end_time = time.time()
                
                recall_time = (end_time - start_time) * 1000  # Convert to ms
                recall_times.append(recall_time)
                total_results += len(results)
                
                if (i + 1) % 100 == 0:
                    avg_so_far = sum(recall_times) / len(recall_times)
                    print(f"    Completed {i + 1:,} recalls, avg: {avg_so_far:.2f}ms")
            
            recall_end = time.time()
            total_recall_time = recall_end - recall_start
            
            # Calculate statistics
            avg_latency = sum(recall_times) / len(recall_times)
            max_latency = max(recall_times)
            min_latency = min(recall_times)
            p95_latency = sorted(recall_times)[int(0.95 * len(recall_times))]
            
            # Get system stats
            stats = memory_manager.stats()
            
            # Compile results
            results = {
                "memory_count": memory_count,
                "recall_queries": recall_queries,
                "storage": {
                    "total_time_sec": round(store_time, 2),
                    "rate_per_sec": round(memory_count / store_time, 0)
                },
                "recall": {
                    "total_time_sec": round(total_recall_time, 2),
                    "avg_latency_ms": round(avg_latency, 2),
                    "max_latency_ms": round(max_latency, 2),
                    "min_latency_ms": round(min_latency, 2),
                    "p95_latency_ms": round(p95_latency, 2),
                    "total_results": total_results,
                    "rate_per_sec": round(recall_queries / total_recall_time, 0)
                },
                "memory_distribution": {
                    "session": stats["session_memory_count"],
                    "core": stats["core_memory_count"],
                    "application": stats["app_memory_count"],
                    "archive": stats["archive_memory_count"],
                    "total": stats["total_memories"]
                },
                "performance_target_met": avg_latency < 50.0
            }
            
            return results
        
    finally:
        # Cleanup test directory
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def print_benchmark_results(results):
    """Print formatted benchmark results"""
    print("🎯 BENCHMARK RESULTS")
    print("=" * 50)
    print(f"Dataset: {results['memory_count']:,} memories")
    print(f"Queries: {results['recall_queries']:,} recalls")
    print()
    
    print("💾 STORAGE PERFORMANCE")
    print(f"  Total time: {results['storage']['total_time_sec']}s")
    print(f"  Rate: {results['storage']['rate_per_sec']:,} memories/sec")
    print()
    
    print("🔍 RECALL PERFORMANCE")
    print(f"  Average latency: {results['recall']['avg_latency_ms']}ms")
    print(f"  P95 latency: {results['recall']['p95_latency_ms']}ms")
    print(f"  Max latency: {results['recall']['max_latency_ms']}ms")
    print(f"  Min latency: {results['recall']['min_latency_ms']}ms")
    print(f"  Rate: {results['recall']['rate_per_sec']:,} recalls/sec")
    print(f"  Total results: {results['recall']['total_results']:,}")
    print()
    
    print("📊 MEMORY DISTRIBUTION")
    dist = results['memory_distribution']
    print(f"  Session: {dist['session']:,}")
    print(f"  Core: {dist['core']:,}")
    print(f"  Application: {dist['application']:,}")
    print(f"  Archive: {dist['archive']:,}")
    print(f"  Total: {dist['total']:,}")
    print()
    
    # Performance assessment
    target_met = results['performance_target_met']
    avg_latency = results['recall']['avg_latency_ms']
    
    if target_met:
        print(f"✅ PERFORMANCE TARGET MET")
        print(f"   Average recall latency {avg_latency}ms < 50ms target")
    else:
        print(f"❌ PERFORMANCE TARGET FAILED")
        print(f"   Average recall latency {avg_latency}ms > 50ms target")
    
    print("=" * 50)
    
    return target_met


def main():
    """Main benchmark execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MemoryHub Performance Benchmark")
    parser.add_argument("--memories", "-m", type=int, default=10000,
                       help="Number of memories to store (default: 10000)")
    parser.add_argument("--recalls", "-r", type=int, default=1000,
                       help="Number of recall operations (default: 1000)")
    parser.add_argument("--quick", action="store_true",
                       help="Quick test with 1000 memories, 100 recalls")
    
    args = parser.parse_args()
    
    if args.quick:
        memory_count = 1000
        recall_count = 100
        print("🚀 Running QUICK benchmark...")
    else:
        memory_count = args.memories
        recall_count = args.recalls
    
    try:
        results = benchmark_memory_operations(memory_count, recall_count)
        target_met = print_benchmark_results(results)
        
        # Exit with appropriate code
        sys.exit(0 if target_met else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Benchmark interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()