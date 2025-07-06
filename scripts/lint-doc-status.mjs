import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Simple linter: ensure every Markdown in docs/ contains <!-- status: ... --> within first 3 lines

const __filename = fileURLToPath(import.meta.url);
const projectRoot = path.resolve(path.dirname(__filename), '..');
const docsDir = path.join(projectRoot, 'docs');

async function collectMarkdownFiles(dir) {
  const mdFiles = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      // Skip archive to avoid scanning massive history
      if (entry.name === 'archive') continue;
      mdFiles.push(...await collectMarkdownFiles(full));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      mdFiles.push(full);
    }
  }
  return mdFiles;
}

async function main() {
  const files = await collectMarkdownFiles(docsDir);
  let hasErr = false;
  for (const f of files) {
    const txt = await fs.readFile(f, 'utf8');
    const firstLines = txt.split('\n').slice(0, 5).join(' ');
    if (!firstLines.match(/<!--\s*status:\s*(draft|in_progress|done|todo)\s*-->/i)) {
      hasErr = true;
      console.error(`❌ Missing or malformed status tag: ${path.relative(projectRoot, f)}`);
    }
  }
  if (hasErr) {
    console.error('\n[lint-doc-status] Some documents are missing status tags.');
    process.exit(1);
  } else {
    console.log('✅ All docs contain valid status tags.');
  }
}

main(); 