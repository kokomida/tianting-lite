import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';
import yaml from 'yaml';

const CONFIG_FILE = path.resolve('tianting.config.yaml');
const TASKS_DIR = path.resolve('tasks');

function sh(cmd, args = []) {
  return new Promise((res, rej) => {
    const p = spawn(cmd, args, { stdio: 'inherit' });
    p.on('exit', code => (code === 0 ? res() : rej(new Error(`${cmd} ${args.join(' ')} exited ${code}`))));
  });
}

async function loadConfig() {
  const raw = await fs.readFile(CONFIG_FILE, 'utf8');
  const cfg = yaml.parse(raw);
  const home = process.env.HOME || process.env.USERPROFILE;
  cfg.workspace_root = cfg.workspace_root.replace('${USER}', path.basename(home));
  return cfg;
}

async function listPendingTasks() {
  const files = await fs.readdir(path.join(TASKS_DIR, 'demo'));
  return files
    .filter(f => f.endsWith('.json'))
    .map(f => path.join(TASKS_DIR, 'demo', f));
}

function buildSystemPrompt(task) {
  return `# OES Task\nID: ${task.id}\nObjective: ${task.objective}\nSuccess Criteria: ${task.success_criteria}`;
}

async function ensureWorkspace(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function cleanupExistingWindows(sessionName) {
  try {
    // Get list of windows in the session
    const result = await new Promise((res, rej) => {
      const p = spawn('tmux', ['list-windows', '-t', sessionName, '-F', '#{window_name}'], { stdio: 'pipe' });
      let output = '';
      p.stdout.on('data', data => output += data.toString());
      p.on('exit', code => code === 0 ? res(output.trim()) : rej(new Error('Failed to list windows')));
    });
    
    if (result) {
      const windows = result.split('\n').filter(w => w.startsWith('demo-'));
      for (const window of windows) {
        try {
          await sh('tmux', ['kill-window', '-t', `${sessionName}:${window}`]);
          console.log(`Killed existing window: ${window}`);
        } catch (e) {
          // Window might already be gone, ignore error
        }
      }
    }
  } catch (e) {
    // Session might not exist yet, ignore error
  }
}

async function ensureTmuxSession(name) {
  try {
    await sh('tmux', ['has-session', '-t', name]);
  } catch {
    await sh('tmux', ['new-session', '-d', '-s', name]);
  }
}

async function launchTask(cfg, taskPath) {
  const raw = await fs.readFile(taskPath, 'utf8');
  const task = JSON.parse(raw);
  const wsDir = path.join(cfg.workspace_root, task.id);
  await ensureWorkspace(wsDir);
  const prompt = buildSystemPrompt(task);
  
  // Start Claude in interactive mode with initial prompt
  await sh('tmux', [
    'new-window',
    '-t', cfg.tmux_session,
    '-n', task.id,
    `bash -c 'cd ${wsDir} && ${cfg.claude_cmd} --dangerously-skip-permissions "${prompt.replace(/"/g, '\\"')}"'`
  ]);
}

async function main() {
  const cfg = await loadConfig();
  await ensureTmuxSession(cfg.tmux_session);
  
  // Clean up any existing demo windows
  await cleanupExistingWindows(cfg.tmux_session);
  
  const tasks = await listPendingTasks();
  const queue = [...tasks];
  const running = new Set();
  async function next() {
    if (queue.length === 0) return;
    if (running.size >= cfg.max_parallel) return;
    const task = queue.shift();
    running.add(task);
    launchTask(cfg, task).then(() => {
      running.delete(task);
      next();
    });
    next();
  }
  next();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {
    console.error(err);
    process.exit(1);
  });
} 