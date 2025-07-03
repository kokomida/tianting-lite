# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tianting-Lite is an AI-driven personal productivity platform that follows the concept "一句话，召唤一支 AI 开发团队" (One sentence, summon an AI development team). It orchestrates multiple AI agents to transform natural language requirements into complete software deliverables.

## Core Architecture

The system follows a 5-module architecture with a 4-layer memory system:

### Main Components
- **Dispatcher**: Parses requirements and generates OES (task specifications)
- **Launcher**: Spawns parallel ClaudeCode windows for task execution
- **Harvester**: Runs CI/testing/quality gates
- **ReviewAgents**: Multi-AI review system for code quality
- **Reporter**: Aggregates artifacts and generates final deliverables
- **MemoryHub**: 4-layer persistent memory system

### Memory Architecture (MemoryHub)
- **Layer 1 (Session)**: Temporary in-memory storage
- **Layer 2 (Core)**: SQLite persistent storage
- **Layer 3 (Application)**: JSONL files for application logs
- **Layer 4 (Archive)**: Compressed storage for long-term retention

## Development Commands

### Node.js/Frontend Commands
```bash
# Install dependencies
pnpm install

# Core application commands
pnpm run plan          # Run task planning (Dispatcher)
pnpm run launch        # Launch ClaudeCode windows
pnpm run harvest       # Run CI/testing pipeline
pnpm run report        # Generate final reports
pnpm run verify-all    # Run all verification steps

# Documentation and linting
pnpm run build-knowledge-index  # Build knowledge base index
pnpm run lint-oes              # Lint OES specifications
pnpm run lint-doc-status       # Check documentation status
```

### Python/MemoryHub Commands
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install MemoryHub package in development mode
pip install -e src/

# Run Python tests
python -m pytest tests/test_memoryhub/

# Run MemoryHub CLI
python scripts/memoryhub_cli.py

# Run benchmarks
python scripts/benchmark_memoryhub.py
```

### Docker Commands
```bash
# Start the full system
docker compose up -d --build

# Quick start example
tianting plan "给我一个 FastAPI Todo Demo"
```

## Key File Locations

- **Core Implementation**: `src/memoryhub/` - Python package for memory management
- **Task Orchestration**: `src/dispatcher/`, `src/launcher/`, `src/harvester/`, `src/reporter/`
- **Configuration**: `tianting.config.yaml`, `package.json`, `src/pyproject.toml`
- **Documentation**: `docs/` - Comprehensive project documentation
- **Tasks**: `tasks/core/` - Task definitions and specifications
- **Tests**: `tests/test_memoryhub/` - Python tests for MemoryHub

## Testing

### Python Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_memoryhub/test_stats.py

# Run tests with coverage
python -m pytest --cov=src/memoryhub tests/
```

### Node.js Tests
```bash
# Run Node.js tests
npm test tests/dispatcher.autoPlan.test.mjs
```

## Code Architecture Notes

### MemoryHub Internal Structure
- `memory_manager.py`: Core LayeredMemoryManager implementation
- `sqlite_dao.py`: SQLite data access layer
- `jsonl_dao.py`: JSONL file operations
- `roaring_bitmap_tag_index.py`: Optimized tagging system using Roaring Bitmaps

### Task Lifecycle States
Tasks progress through: PENDING → RUNNING → TESTING → REVIEW → PACKAGING → DONE
Alternative paths: FIX (re-run) or REJECTED (manual intervention)

### OES (Object-Event-State) Specification
Tasks are defined using OES format in JSON, specifying role, type, object, and prompt for each AI agent.

## Common Development Patterns

- All Python code follows the layered architecture pattern
- Memory operations should go through the LayeredMemoryManager
- Task definitions use OES JSON format
- Documentation follows the numbered chapter system (00-roadmap.md through 11-glossary.md)
- Git workflow uses feature branches with descriptive names like `feat/core-03a-roaring-bitmap`

## Important Notes

- The system is designed for local execution with no telemetry by default
- MemoryHub data is stored in `memoryhub_data/` directory
- The project uses both Node.js (orchestration) and Python (memory management) components
- All AI agent interactions are logged for audit and learning purposes