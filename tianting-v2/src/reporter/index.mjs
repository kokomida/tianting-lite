import fs from 'fs/promises';
import path from 'path';
import yaml from 'yaml';
import archiver from 'archiver';
import { createWriteStream } from 'fs';

const CONFIG_FILE = path.resolve('tianting.config.yaml');
const DELIVERY_DIR = path.resolve('delivery');
const TASKS_DIR = path.resolve('tasks/demo');

async function loadConfig() {
  const raw = await fs.readFile(CONFIG_FILE, 'utf8');
  const cfg = yaml.parse(raw);
  const home = process.env.HOME || process.env.USERPROFILE;
  cfg.workspace_root = cfg.workspace_root.replace('${USER}', path.basename(home));
  return cfg;
}

async function readTasks() {
  const files = (await fs.readdir(TASKS_DIR)).filter(f=>f.endsWith('.json'));
  const tasks = [];
  for (const f of files) {
    const data = JSON.parse(await fs.readFile(path.join(TASKS_DIR, f), 'utf8'));
    tasks.push(data);
  }
  return tasks;
}

function statusIcon(status){
  switch(status){
    case 'verified': return '✅';
    case 'tests_passed': return '🔵';
    case 'failed': return '❌';
    default: return '⏳';
  }
}

async function genReportMarkdown(tasks) {
  const lines = [];
  lines.push('# Tianting Delivery Report');
  lines.push('');
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push('');
  lines.push('| Task | Status | Objective |');
  lines.push('|------|--------|-----------|');
  for (const t of tasks) {
    lines.push(`| ${t.id} | ${statusIcon(t.status)} ${t.status||'pending'} | ${t.objective} |`);
  }
  lines.push('');
  return lines.join('\n');
}

async function createZip(sourceDir, outPath) {
  await fs.mkdir(path.dirname(outPath), { recursive: true });
  return new Promise((res, rej) => {
    const output = createWriteStream(outPath);
    const archive = archiver('zip', { zlib: { level: 9 } });
    output.on('close', () => res());
    archive.on('error', err => rej(err));
    archive.pipe(output);
    archive.directory(sourceDir, false);
    archive.finalize();
  });
}

async function main() {
  const cfg = await loadConfig();
  const tasks = await readTasks();
  await fs.mkdir(DELIVERY_DIR, { recursive: true });
  const reportMd = await genReportMarkdown(tasks);
  await fs.writeFile(path.join(DELIVERY_DIR, 'report.md'), reportMd);
  const zipPath = path.join(DELIVERY_DIR, 'project.zip');
  await createZip(cfg.workspace_root, zipPath);
  console.log('[reporter] report generated at delivery/report.md');
  console.log('[reporter] workspace archived at delivery/project.zip');
  if (tasks.some(t=>t.status==='failed' || t.status!=='verified')) {
    console.error('[reporter] some tasks not verified');
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {console.error(err); process.exit(1);});
} 