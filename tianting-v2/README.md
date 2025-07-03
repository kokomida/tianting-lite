# Tianting-Lite (v0.2-MVP)

AI-driven personal productivity platform —— "一句话，召唤一支 AI 开发团队"。

## 🚀 Quick Start (Local)
```bash
pnpm install
docker compose up -d --build
tianting plan "给我一个 FastAPI Todo Demo"
```

## 🧠 MemoryHub Installation (Python Component)

MemoryHub provides persistent memory management for AI agents with 4-layer architecture and high-performance indexing.

### Prerequisites
- Python 3.8+
- Linux/macOS/WSL2 (for optimal performance)
- Boost libraries (for PyRoaring bitmap support)

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libboost-dev python3-dev build-essential
```

**macOS:**
```bash
brew install boost python3-dev
```

**WSL2/Windows:**
```bash
# In WSL2 Ubuntu
sudo apt-get update
sudo apt-get install -y libboost-dev python3-dev build-essential
```

### Python Installation
```bash
cd tianting-v2

# Install dependencies
pip install -r requirements.txt

# Install MemoryHub in development mode
pip install -e src/

# Run tests
python -m pytest tests/

# Run benchmark
python scripts/benchmark_memoryhub.py --quick --index roaring
```

### Performance Targets
- **Storage**: >500 memories/sec
- **Recall**: <35ms average latency
- **Memory**: 50-80% reduction with Roaring Bitmap indexing
- **Cross-platform**: Windows/Linux/macOS compatibility

### CLI Usage
```bash
# Show memory statistics
memoryhub stats

# Run performance benchmark
memoryhub benchmark --memories 10000 --recalls 500

# Build search index
memoryhub build-index

# Show system info
memoryhub info
```

## 📚 Documentation
- 版本路线图 & 章节索引：`docs/index.md`
- 术语表：`docs/11-glossary.md`
- 历史蓝皮书 & 决策记录：`docs/archive/`

## 🗂️ Repo Layout (trimmed)
| Path | Purpose |
|------|---------|
| `docs/` | All project documents (00–10) & changelogs |
| `scripts/` | Utility scripts (doc index, lint, etc.) |
| `src/` | Future core implementation (dispatcher, launcher, …) |
| `samples/` | Test fixtures & monitoring logs (coming soon) |

---
*Initialized 2025-07-04 – Maintained by AI PM & Developer Assistants*
*Last updated 2025-07-05 – Maintained by AI PM & Developer Assistants* 