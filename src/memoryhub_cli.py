#!/usr/bin/env python3
"""
MemoryHub CLI Tools
Provides command-line utilities for MemoryHub management
"""
import sys
import os
import argparse
import json
from pathlib import Path

from memoryhub import LayeredMemoryManager
from memoryhub.jsonl_dao import JSONLMemoryDAO


def build_index_command(args):
    """Build or rebuild JSONL indices"""
    data_path = args.data_path or "./memoryhub_data"
    
    print(f"🔨 Building MemoryHub indices in: {data_path}")
    
    # Initialize DAO
    dao = JSONLMemoryDAO(data_path)
    
    # Determine which layers to build
    layers_to_build = []
    if args.layer:
        if args.layer in ["application", "archive"]:
            layers_to_build = [args.layer]
        else:
            print(f"❌ Invalid layer: {args.layer}. Must be 'application' or 'archive'")
            return 1
    else:
        layers_to_build = ["application", "archive"]
    
    # Build indices
    success_count = 0
    for layer in layers_to_build:
        print(f"  📁 Building index for {layer} layer...")
        
        if dao.build_index(layer, force_rebuild=args.force):
            # Get stats
            cache = dao._get_index_cache(layer)
            entry_count = len(cache) if cache else 0
            
            # Get file paths for size info
            if layer == "application":
                jsonl_file = dao.app_logs_file
                index_file = dao.app_logs_index
            else:
                jsonl_file = dao.archive_file
                index_file = dao.archive_index
            
            jsonl_size = jsonl_file.stat().st_size if jsonl_file.exists() else 0
            index_size = index_file.stat().st_size if index_file.exists() else 0
            
            print(f"     ✅ {layer}: {entry_count:,} entries indexed")
            print(f"        JSONL: {jsonl_size:,} bytes")
            print(f"        Index: {index_size:,} bytes")
            success_count += 1
        else:
            print(f"     ❌ Failed to build index for {layer}")
    
    if success_count == len(layers_to_build):
        print(f"🎯 Successfully built {success_count}/{len(layers_to_build)} indices")
        return 0
    else:
        print(f"⚠️  Built {success_count}/{len(layers_to_build)} indices with errors")
        return 1


def stats_command(args):
    """Show MemoryHub statistics"""
    data_path = args.data_path or "./memoryhub_data"
    
    print(f"📊 MemoryHub Statistics: {data_path}")
    print("=" * 50)
    
    try:
        manager = LayeredMemoryManager(path=data_path)
        stats = manager.stats()
        
        print(f"📈 Memory Counts:")
        print(f"  Session: {stats['session_memory_count']:,}")
        print(f"  Core: {stats['core_memory_count']:,}")
        print(f"  Application: {stats['app_memory_count']:,}")
        print(f"  Archive: {stats['archive_memory_count']:,}")
        print(f"  Total: {stats['total_memories']:,}")
        print()
        
        print(f"⚡ Performance:")
        perf = stats['performance']
        print(f"  Avg Recall Latency: {perf['avg_recall_latency_ms']:.2f}ms")
        print(f"  Max Recall Latency: {perf['max_recall_latency_ms']:.2f}ms")
        print(f"  Total Recalls: {perf['recall_count']:,}")
        print()
        
        if args.verbose:
            print(f"🗄️  Database Stats:")
            db_stats = stats.get('db_stats', {})
            for key, value in db_stats.items():
                if key != 'tables':
                    print(f"  {key}: {value}")
            
            print(f"📄 JSONL Stats:")
            jsonl_stats = stats.get('jsonl_stats', {})
            for key, value in jsonl_stats.items():
                if key != 'files':
                    print(f"  {key}: {value}")
        
        manager.close()
        return 0
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return 1


def flush_command(args):
    """Flush pending recall count updates"""
    data_path = args.data_path or "./memoryhub_data"
    
    print(f"💾 Flushing pending updates: {data_path}")
    
    try:
        manager = LayeredMemoryManager(path=data_path)
        manager.flush_pending_updates()
        print("✅ Successfully flushed pending updates")
        manager.close()
        return 0
        
    except Exception as e:
        print(f"❌ Error flushing updates: {e}")
        return 1


def benchmark_command(args):
    """Run MemoryHub benchmark"""
    data_path = args.data_path or "./memoryhub_data"
    
    print(f"🚀 Running MemoryHub benchmark")
    print(f"📊 Memories: {args.memories:,}, Recalls: {args.recalls:,}")
    
    try:
        # Import benchmark function
        script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        sys.path.insert(0, script_dir)
        from benchmark_memoryhub import benchmark_memory_operations, print_benchmark_results
        
        results = benchmark_memory_operations(args.memories, args.recalls)
        target_met = print_benchmark_results(results)
        
        return 0 if target_met else 1
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        return 1


def info_command(args):
    """Show MemoryHub information"""
    data_path = args.data_path or "./memoryhub_data"
    
    print(f"📊 MemoryHub Information: {data_path}")
    print("=" * 50)
    
    # Initialize DAO
    dao = JSONLMemoryDAO(data_path)
    
    for layer in ["application", "archive"]:
        print(f"\n📁 {layer.upper()} Layer:")
        
        # Get file paths
        if layer == "application":
            jsonl_file = dao.app_logs_file
            index_file = dao.app_logs_index
        else:
            jsonl_file = dao.archive_file
            index_file = dao.archive_index
        
        # JSONL file info
        if jsonl_file.exists():
            jsonl_size = jsonl_file.stat().st_size
            jsonl_mtime = jsonl_file.stat().st_mtime
            print(f"  📄 JSONL: {jsonl_size:,} bytes (modified: {jsonl_mtime})")
        else:
            print(f"  📄 JSONL: Not found")
        
        # Index file info
        if index_file.exists():
            index_size = index_file.stat().st_size
            index_mtime = index_file.stat().st_mtime
            
            # Load index to count entries
            cache = dao._get_index_cache(layer)
            entry_count = len(cache) if cache else 0
            
            print(f"  🗂️  Index: {index_size:,} bytes, {entry_count:,} entries (modified: {index_mtime})")
            
            # Check if index is up to date
            if jsonl_file.exists() and index_mtime < jsonl_mtime:
                print(f"  ⚠️  Index is outdated (JSONL modified after index)")
            else:
                print(f"  ✅ Index is up to date")
        else:
            print(f"  🗂️  Index: Not found")
            if jsonl_file.exists():
                print(f"  💡 Run 'build-index' to create index")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="MemoryHub CLI Tools",
        prog="memoryhub"
    )
    
    parser.add_argument(
        "--data-path", "-d",
        help="Path to MemoryHub data directory (default: ./memoryhub_data)",
        default=None
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Build index command
    build_parser = subparsers.add_parser(
        "build-index",
        help="Build or rebuild JSONL indices for fast search"
    )
    build_parser.add_argument(
        "--layer", "-l",
        choices=["application", "archive"],
        help="Specific layer to build (default: all layers)"
    )
    build_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force rebuild even if index is up to date"
    )
    build_parser.set_defaults(func=build_index_command)
    
    # Stats command
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show MemoryHub statistics and performance metrics"
    )
    stats_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed statistics"
    )
    stats_parser.set_defaults(func=stats_command)
    
    # Flush command
    flush_parser = subparsers.add_parser(
        "flush",
        help="Flush pending recall count updates to disk"
    )
    flush_parser.set_defaults(func=flush_command)
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Run MemoryHub performance benchmark"
    )
    benchmark_parser.add_argument(
        "--memories", "-m",
        type=int,
        default=1000,
        help="Number of memories to store (default: 1000)"
    )
    benchmark_parser.add_argument(
        "--recalls", "-r",
        type=int,
        default=100,
        help="Number of recall operations (default: 100)"
    )
    benchmark_parser.set_defaults(func=benchmark_command)
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show MemoryHub file information and status"
    )
    info_parser.set_defaults(func=info_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())