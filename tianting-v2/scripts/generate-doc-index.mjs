#!/usr/bin/env node
import { promises as fs } from 'fs';
import path from 'path';

const DOCS_DIR = path.resolve(process.cwd(), 'tianting-v2', 'docs');
const INDEX_FILE = path.join(DOCS_DIR, 'index.md');

const statusEmoji = {
  done: '✅',
  in_progress: '🟡',
  draft: '📝',
  todo: '⛔'
};

async function main() {
  const entries = await fs.readdir(DOCS_DIR);
  const rows = [];
  for (const file of entries) {
    if (!/^\d{2}.*\.md$/.test(file)) continue;
    const content = await fs.readFile(path.join(DOCS_DIR, file), 'utf8');
    const statusMatch = content.match(/status:\s*(done|in_progress|draft|todo)/i);
    const statusKey = statusMatch ? statusMatch[1].toLowerCase() : 'draft';
    const status = statusEmoji[statusKey] || '📝';
    rows.push({ file, status });
  }
  rows.sort();
  const table = rows
    .map(({ file, status }) => {
      const num = file.split('-')[0];
      return `| ${num} | ${file} |  | ${status} |`;
    })
    .join('\n');

  const md = `# Documentation Index\n\n| # | File | Description | Status |\n|---|------|-------------|--------|\n${table}\n`;
  await fs.writeFile(INDEX_FILE, md);
  console.log('docs/index.md regenerated');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
}); 