"""
MemoryHub - Layered Memory Management for Tianting-v2

Four-layer memory architecture:
- Session Layer (Layer-1): Temporary in-memory storage
- Core Layer (Layer-2): SQLite persistent storage for tasks/windows
- Application Layer (Layer-3): JSONL files for logs and traces
- Archive Layer (Layer-4): Compressed historical data
"""

from .memory_manager import LayeredMemoryManager

__version__ = "0.2.0"
__all__ = ["LayeredMemoryManager"]