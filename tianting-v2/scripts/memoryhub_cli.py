#!/usr/bin/env python3
"""
MemoryHub CLI Tools
Provides command-line utilities for MemoryHub management
"""
import sys
import os
import argparse
from pathlib import Path

# Add src to path to import memoryhub
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show MemoryHub status and statistics"
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