# Contributing to Tianting-v2

## Development Setup

1. **Prerequisites**
   - Node.js >= 18.0.0
   - Python >= 3.10
   - pnpm >= 8.0.0
   - Claude Code CLI

2. **Installation**
   ```bash
   git clone https://github.com/kokomida/tianting-lite.git
   cd tianting-v2
   pnpm install
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Development Workflow

### Branch Strategy
- `main` - Production ready code
- `develop` - Development integration branch  
- `feature/*` - Feature development
- `hotfix/*` - Critical fixes

### Commit Convention
We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new dispatcher module
fix: resolve harvester memory leak
docs: update API documentation
chore: update dependencies
```

### Before Committing
```bash
# Run all linting
pnpm run lint

# Run tests
pnpm test

# Generate doc index
node scripts/generate-doc-index.mjs
```

### Release Process
```bash
# Bump version and generate changelog
pnpm run release

# Push tags
git push --follow-tags origin main
```

## Code Style

### OES Task Format
- All tasks must validate against the JSON Schema in `docs/06-oes-spec.md`
- Use `pnpm run lint-oes` to validate

### Documentation
- Follow the status tags: `<!-- status: draft|in_progress|done|todo -->`
- Use `pnpm run lint-doc-status` to validate

### Architecture Principles
1. **Modularity**: Each module should be independently testable
2. **Error Handling**: Graceful degradation with meaningful error messages  
3. **Observability**: Log key events and metrics
4. **Security**: Never commit secrets or API keys

## Testing

### Unit Tests
```bash
# Run specific test
node tests/dispatcher.autoPlan.test.mjs

# Add new tests in tests/ directory
```

### Integration Tests
```bash
# Full pipeline test
pnpm run verify-all
```

## Documentation

### Adding New Docs
1. Create in appropriate `docs/` subdirectory
2. Add front matter with status
3. Update `docs/index.md` 
4. Run `node scripts/generate-doc-index.mjs`

### Knowledge Cards
- Place in `docs/knowledge/YYYY/MM/DD/`
- Follow the learning schema
- Validate with `pnpm run lint-learning-schema`

## Security

- **Never commit `.env` files**
- **Use `.env.example` for templates**
- **Rotate API keys regularly**
- **Review code for hardcoded secrets**

## Getting Help

- Check existing issues on GitHub
- Review documentation in `docs/`
- Ask questions in discussions