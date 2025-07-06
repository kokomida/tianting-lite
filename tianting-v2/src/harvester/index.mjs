import chokidar from 'chokidar';
import { spawn } from 'child_process';
import path from 'path';
import yaml from 'yaml';
import fs from 'fs/promises';
import { verifyWorkspace } from '../verifier/index.mjs';

const CONFIG_FILE = path.resolve('tianting.config.yaml');

function sh(cmd, args, cwd) {
  return new Promise((res, rej) => {
    const p = spawn(cmd, args, { stdio: 'inherit', cwd });
    p.on('exit', code => (code === 0 ? res() : rej(new Error(`${cmd} exited ${code}`))));
  });
}

async function loadConfig() {
  const raw = await fs.readFile(CONFIG_FILE, 'utf8');
  const cfg = yaml.parse(raw);
  const home = process.env.HOME || process.env.USERPROFILE;
  cfg.workspace_root = cfg.workspace_root.replace('${USER}', path.basename(home));
  return cfg;
}

async function runTests(dir) {
  try {
    await sh('pytest', ['-q'], dir);
    console.log(`[harvester] tests passed in ${dir}`);
    const taskId = path.basename(dir);
    const taskFile = await findTaskFile(taskId);
    if (taskFile) {
      await updateTaskStatus(taskFile, { status: 'tests_passed', tests_passed_at: new Date().toISOString() });
    }
    await verifyWorkspace(dir);
  } catch (e) {
    console.error(`[harvester] tests failed in ${dir}`);
    const taskId = path.basename(dir);
    const taskFile = await findTaskFile(taskId);
    if (taskFile) {
      await updateTaskStatus(taskFile, { status: 'failed', failed_at: new Date().toISOString(), fail_reason: e.message });
    }
  }
}

async function findTaskFile(taskId) {
  const taskDir = path.resolve('tasks/demo');
  const files = (await fs.readdir(taskDir)).filter(f=>f.endsWith('.json'));
  for (const f of files) {
    const p = path.join(taskDir, f);
    const data = JSON.parse(await fs.readFile(p, 'utf8'));
    if (data.id === taskId) return p;
  }
  return null;
}

async function updateTaskStatus(taskPath, updates) {
  const data = JSON.parse(await fs.readFile(taskPath, 'utf8'));
  Object.assign(data, updates);
  await fs.writeFile(taskPath, JSON.stringify(data, null, 2));
}

async function main() {
  const cfg = await loadConfig();
  const watcher = chokidar.watch(cfg.workspace_root, { ignoreInitial: true });
  watcher.on('all', (event, filePath) => {
    if (['add', 'change'].includes(event) && filePath.endsWith('.py')) {
      const taskDir = path.dirname(filePath);
      runTests(taskDir);
    }
  });
  console.log('[harvester] watching', cfg.workspace_root);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
} 