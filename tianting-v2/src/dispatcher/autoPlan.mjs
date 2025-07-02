import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

const demoTemplates = {
  'fastapi todo demo': {
    modulePrefix: 'demo',
    tasks: [
      {
        role: 'python-backend-developer',
        object: 'FastAPITodo',
        event: 'create_crud_endpoints',
        type: 'CODE',
        prompt: '使用 FastAPI 实现 /todos CRUD，返回 JSON，使用 SQLite 内存 DB。',
        success_criteria: 'pytest 全绿'
      },
      {
        role: 'python-backend-developer',
        object: 'FastAPITodo',
        event: 'write_tests',
        type: 'TEST',
        prompt: '为 CRUD 端点编写 pytest 单元测试，覆盖率 ≥ 80%。',
        success_criteria: 'coverage ≥ 80%'
      },
      {
        role: 'devops-engineer',
        object: 'FastAPITodo',
        event: 'dockerize',
        type: 'DOC',
        prompt: '编写 Dockerfile 和 docker-compose.yml，端口 8000。',
        success_criteria: '容器启动 curl /healthz 200'
      }
    ]
  }
};

export async function autoPlan(sentence, maxParallel = 3, outDir = 'tasks/demo') {
  const key = Object.keys(demoTemplates).find(k => sentence.toLowerCase().includes(k));
  if (!key) throw new Error('No template matched for sentence');
  const tpl = demoTemplates[key];
  const tasksOutputDir = path.resolve(outDir);
  await fs.mkdir(tasksOutputDir, { recursive: true });

  const created = [];
  for (let i = 0; i < tpl.tasks.length; i++) {
    const t = tpl.tasks[i];
    const id = `${tpl.modulePrefix}-${String(i + 1).padStart(2, '0')}`;
    const filename = path.join(tasksOutputDir, `${id}-${t.role}.task.json`);
    const task = {
      id,
      module: tpl.modulePrefix,
      role: t.role,
      objective: `${t.object} – ${t.event}`,
      environment: 'local-dev',
      implementation_guide: t.prompt,
      success_criteria: t.success_criteria,
      status: 'pending',
      priority: 'P1',
      retry: 1,
      tags: ['demo'],
      created_at: new Date().toISOString()
    };
    await fs.writeFile(filename, JSON.stringify(task, null, 2));
    created.push(filename);
  }
  // write plan markdown
  const planMd = `# Plan for "${sentence}"

- Total tasks: ${created.length}
- Max parallel: ${maxParallel}

${created.map(f=>`- [ ] ${path.basename(f)}`).join('\n')}
`;
  await fs.writeFile(path.join(tasksOutputDir, 'PLAN.md'), planMd);

  return created;
}

// CLI usage: node autoPlan.mjs "sentence" [maxParallel]
if (import.meta.url === `file://${process.argv[1]}`) {
  const sentence = process.argv[2];
  if (!sentence) {
    console.error('Usage: node autoPlan.mjs "sentence"');
    process.exit(1);
  }
  const maxP = process.argv[3] ? Number(process.argv[3]) : 3;
  autoPlan(sentence, maxP).then(list => {
    console.log('Created tasks:', list.map(p=>path.relative(process.cwd(),p)).join('\n'));
  }).catch(err => {
    console.error(err);
    process.exit(1);
  });
} 