import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const projectRoot = path.resolve(path.dirname(__filename), '..');
const specPath = path.join(projectRoot, 'docs', '05-detailed-design.md');

async function extractSchema() {
  const md = await fs.readFile(specPath, 'utf8');
  const match = md.match(/```json\s*<!--\s*learning-output-schema\s*-->\s*([\s\S]*?)```/);
  if (!match) throw new Error('Learning output JSON schema not found in 05-detailed-design.md');
  return JSON.parse(match[1]);
}

async function collectJson(startDir) {
  const arr = [];
  async function walk(dir) {
    const ents = await fs.readdir(dir, { withFileTypes: true });
    for (const e of ents) {
      if (e.name.startsWith('.')) continue;
      const p = path.join(dir, e.name);
      if (e.isDirectory()) await walk(p);
      else if (e.isFile() && e.name.endsWith('.json') && p.includes(`${path.sep}knowledge${path.sep}`)) {
        arr.push(p);
      }
    }
  }
  await walk(path.join(projectRoot, 'docs', 'knowledge'));
  return arr;
}

async function main() {
  let schema;
  try { schema = await extractSchema(); } catch (e) { console.error(e.message); process.exit(1);}  
  const Ajv = (await import('ajv')).default; const ajv = new Ajv({ allErrors:true}); const validate = ajv.compile(schema);
  const files = await collectJson();
  if (files.length === 0) { console.log('[lint-learning] No learning JSON found, skip'); return; }
  let err=false;
  for (const f of files) {
    try { const data = JSON.parse(await fs.readFile(f,'utf8')); const ok=validate(data); if(!ok){err=true; console.error(`❌ ${f}`); console.error(validate.errors);} else console.log(`✅ ${f}`);} catch(e){err=true; console.error(`❌ ${f} – ${e.message}`);} }
  if (err){console.error('Validation failed'); process.exit(1);} else console.log('All learning outputs valid');
}
main(); 