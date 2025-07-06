# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tianting-Lite v0.2 is an AI-driven personal productivity platform that implements "一句话，召唤一支 AI 开发团队" (One sentence summons an AI development team). It's a pipeline system that takes natural language requirements and automatically generates, tests, and delivers code solutions.

## Common Development Commands

### Environment Setup
- `pnpm install` - Install Node.js dependencies
- `pip install -r requirements.txt` - Install Python dependencies
- `cp .env.example .env` - Set up environment variables (requires API keys)

### Core Workflow Commands
- `pnpm start` - Run complete pipeline (same as verify-all)
- `pnpm verify-all` - Run complete pipeline (Dispatcher → Launcher → Harvester → Verifier → Reporter)
- `pnpm plan` - Generate task planning from requirements using autoPlan dispatcher
- `pnpm launch` - Launch Claude Code instances in tmux windows for pending tasks
- `pnpm harvest` - Monitor workspace changes and run tests automatically
- `pnpm report` - Generate delivery report and archive workspace

### Development Commands
- `pnpm dev` - Development mode (runs launcher)
- `pnpm test` - Run dispatcher auto-planning tests
- `pnpm lint` - Run all linting checks (OES, docs, learning schema)

### Utility Scripts
- `pnpm lint-oes` - Validate OES (Objective-Event-System) task definitions
- `pnpm lint-doc-status` - Check documentation status and consistency
- `pnpm lint-learning-schema` - Validate learning schema
- `pnpm build-knowledge-index` - Build searchable knowledge base index

### Python MemoryHub CLI
- `python src/memoryhub_cli.py build-index` - Build MemoryHub JSONL indices
- `python src/memoryhub_cli.py build-index --force` - Force rebuild indices
- `python src/memoryhub_cli.py build-index --layer application` - Build specific layer index

### Testing
- `node tests/dispatcher.autoPlan.test.mjs` - Test the auto-planning functionality
- `pytest` - Run Python tests (used by harvester for verification)

### Docker Deployment
- `docker compose up -d --build` - Start complete local stack

## Architecture Overview

The system follows a 5-module pipeline architecture:

1. **Dispatcher** (`src/dispatcher/autoPlan.mjs`) - Parses natural language requirements and generates OES task definitions
2. **Launcher** (`src/launcher/index.mjs`) - Spawns parallel Claude Code instances in tmux windows for task execution
3. **Harvester** (`src/harvester/index.mjs`) - Monitors file changes and triggers automated testing
4. **Verifier** (`src/verifier/index.mjs`) - Runs acceptance tests and validation stages
5. **Reporter** (`src/reporter/index.mjs`) - Generates final delivery reports and archives

### Key Configuration
- `tianting.config.yaml` - Runtime configuration (workspace paths, tmux session, parallel limits)
- `tasks/demo/` - Task definitions in OES JSON format
- `delivery/` - Output directory for reports and project archives

### Task Definition Format
Tasks use the OES (Objective-Event-System) format with these key fields:
- `id` - Unique task identifier (e.g., "demo-01")
- `role` - Target role (e.g., "python-backend-developer", "devops-engineer")
- `objective` - What needs to be accomplished
- `implementation_guide` - Detailed instructions
- `success_criteria` - How success is measured
- `verification.stages` - Multi-stage verification process

### Verification Stages
The verifier supports multiple stage types:
- `shell` - Execute shell commands
- `unit` - Run unit tests
- `compose` - Docker compose up/down with health checks

## Development Patterns

### Adding New Task Templates
Edit `src/dispatcher/autoPlan.mjs` and add to the `demoTemplates` object with appropriate role mappings and task sequences.

### Extending Verification
Tasks can define custom verification stages in their JSON files under the `verification.stages` array.

### Memory and State Management
The system uses SQLite for task state persistence and JSONL for logging. The MemoryHub concept (referenced in docs) provides four-layer memory architecture:

- **Application Layer** - Real-time application events and interactions
- **Archive Layer** - Long-term historical data storage
- **Tag Index** - Fast retrieval via Roaring bitmap indexing
- **CLI Tools** - Python-based utilities for index management

## File Structure Notes

- `docs/` - Comprehensive project documentation following numbered sequence (00-11)
- `scripts/` - Utility scripts for maintenance and linting
- `samples/` - Test fixtures and examples
- `normaldocs/` - Additional technical documentation
- `main.py` - FastAPI Todo demo implementation (example output)

## Important Constraints

- The system is designed to work with Claude Code CLI (`claude` command)
- Uses tmux for session management and parallel execution
- Python components expect pytest for testing
- Docker integration available but optional for development
- Requires API keys configured in `.env` file (OpenAI-compatible endpoints)
- Node.js ≥18.0.0 and pnpm ≥8.0.0 required
- Python components use FastAPI, uvicorn, and pysimdjson

## Environment Variables

Key environment variables (from `.env.example`):
- `OPENAI_API_KEY` - API key for AI model access
- `OPENAI_BASE_URL` - API endpoint (defaults to SiliconFlow)
- `DEFAULT_MODEL` - AI model to use (e.g., Pro/deepseek-ai/DeepSeek-R1)
- `WORKSPACE_ROOT` - Root directory for generated projects
- `CLAUDE_CMD` - Claude Code CLI command path
- `MAX_PARALLEL` - Maximum parallel task execution limit