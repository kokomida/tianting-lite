import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), '..');
const knowledgeDir = path.join(root, 'docs', 'knowledge');
const indexPath = path.join(knowledgeDir, 'index.json');

async function gatherCards() {
  const entries = [];
  async function walk(dir) {
    for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) await walk(p);
      else if (entry.isFile() && entry.name.endsWith('.md')) {
        const txt = await fs.readFile(p, 'utf8');
        const lines = txt.split('\n');
        const titleLine = lines.find(l => l.startsWith('# ')) || '# (untitled)';
        const title = titleLine.replace(/^# /, '').trim();
        const addedMatch = txt.match(/\*added_at:\s*([0-9-]+)\*/);
        const added_at = addedMatch ? addedMatch[1] : null;
        entries.push({ title, path: path.relative(knowledgeDir, p).replace(/\\/g, '/'), added_at });
      }
    }
  }
  await walk(knowledgeDir);
  return entries.sort((a,b)=>a.title.localeCompare(b.title));
}

async function main() {
  const cards = await gatherCards();
  await fs.writeFile(indexPath, JSON.stringify(cards, null, 2), 'utf8');
  console.log(`✅ Knowledge index written: ${path.relative(root, indexPath)} (${cards.length} cards)`);
}

main(); 