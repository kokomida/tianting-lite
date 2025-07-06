import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';
import yaml from 'yaml';

const CONFIG_FILE = path.resolve('tianting.config.yaml');
const TASKS_DIR = path.resolve('tasks/demo');

async function loadConfig() {
  const raw = await fs.readFile(CONFIG_FILE, 'utf8');
  const cfg = yaml.parse(raw);
  const home = process.env.HOME || process.env.USERPROFILE;
  cfg.workspace_root = cfg.workspace_root.replace('${USER}', path.basename(home));
  return cfg;
}

function shTimeout(cmd, cwd, timeout = 300000) {
  return new Promise((res, rej) => {
    const child = spawn('bash', ['-c', cmd], { cwd, stdio: 'inherit' });
    const timer = setTimeout(() => {
      child.kill('SIGKILL');
      rej(new Error(`Verifier timeout after ${timeout} ms`));
    }, timeout);
    child.on('exit', code => {
      clearTimeout(timer);
      code === 0 ? res() : rej(new Error(`Verifier exited with code ${code}`));
    });
  });
}

async function findTaskFileById(id) {
  const files = await fs.readdir(TASKS_DIR);
  for (const f of files) {
    if (f.endsWith('.json')) {
      const p = path.join(TASKS_DIR, f);
      const data = JSON.parse(await fs.readFile(p, 'utf8'));
      if (data.id === id) return p;
    }
  }
  return null;
}

async function updateTaskStatus(taskPath, updates) {
  const data = JSON.parse(await fs.readFile(taskPath, 'utf8'));
  Object.assign(data, updates);
  await fs.writeFile(taskPath, JSON.stringify(data, null, 2));
}

async function runStage(stage, cwd) {
  const type = stage.type || 'shell';
  switch(type){
    case 'shell':
      await shTimeout(stage.cmd, cwd, (stage.timeout||300)*1000);
      break;
    case 'unit':
      await shTimeout(stage.cmd, cwd, (stage.timeout||300)*1000);
      break;
    case 'compose': {
      const file = stage.file || 'docker-compose.yml';
      const upCmd = `docker compose -f ${file} up --build -d`;
      await shTimeout(upCmd, cwd, (stage.timeout||600)*1000);
      if (Array.isArray(stage.health)) {
        for (const url of stage.health) {
          await shTimeout(`curl -f --retry 5 --retry-all-errors ${url}`, cwd, 60000);
        }
      }
      const downCmd = `docker compose -f ${file} down -v`;
      await shTimeout(downCmd, cwd, 300000);
      break;}
    default:
      throw new Error(`Unknown stage type ${type}`);
  }
}

export async function verifyWorkspace(workspaceDir) {
  const id = path.basename(workspaceDir);
  const taskPath = await findTaskFileById(id);
  if (!taskPath) {
    console.error(`[verifier] task file not found for id ${id}`);
    return;
  }
  const task = JSON.parse(await fs.readFile(taskPath, 'utf8'));
  const verification = task.verification;
  if (verification && Array.isArray(verification.stages)) {
    const timeoutGlobal = (verification.timeout||1800)*1000;
    const start = Date.now();
    try {
      for (const stage of verification.stages) {
        console.log(`[verifier] running stage ${stage.type||'shell'} for ${id}`);
        await runStage(stage, workspaceDir);
        if(Date.now()-start>timeoutGlobal){
          throw new Error('verification global timeout');
        }
      }
      await updateTaskStatus(taskPath, { status: 'verified', verified_at: new Date().toISOString() });
      console.log(`[verifier] task ${id} verified ✅`);
    } catch (e) {
      console.error(`[verifier] task ${id} failed ❌`, e.message);
      await fs.writeFile(path.join(workspaceDir, '.tianting-error.log'), e.stack || e.message);
      await updateTaskStatus(taskPath, { status: 'failed', failed_at: new Date().toISOString(), fail_reason: e.message });
    }
    return;
  }
  // fallback to acceptance
  const acceptance = task.acceptance;
  if (!acceptance || !acceptance.cmd) {
    console.log(`[verifier] no acceptance or verification defined for ${id}, skipping`);
    await updateTaskStatus(taskPath, { status: 'verified', verified_at: new Date().toISOString() });
    return;
  }
  const timeoutMs = (acceptance.timeout || 300) * 1000;
  try {
    console.log('[verifier] running acceptance for', id);
    await shTimeout(acceptance.cmd, workspaceDir, timeoutMs);
    await updateTaskStatus(taskPath, { status: 'verified', verified_at: new Date().toISOString() });
    console.log(`[verifier] task ${id} verified ✅`);
  } catch (e) {
    console.error(`[verifier] task ${id} failed ❌`, e.message);
    await fs.writeFile(path.join(workspaceDir, '.tianting-error.log'), e.stack || e.message);
    await updateTaskStatus(taskPath, { status: 'failed', failed_at: new Date().toISOString(), fail_reason: e.message });
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const dir = process.argv[2];
  if (!dir) {
    console.error('Usage: node src/verifier/index.mjs <workspaceDir>');
    process.exit(1);
  }
  verifyWorkspace(dir).catch(err => { console.error(err); process.exit(1); });
} 