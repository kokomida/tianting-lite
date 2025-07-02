import { autoPlan } from '../src/dispatcher/autoPlan.mjs';
import fs from 'fs/promises';
import path from 'path';
import assert from 'assert';

(async () => {
  const tempDir = path.join('.tmp-test', 'tasks');
  await fs.rm(tempDir, { recursive: true, force: true });
  const files = await autoPlan('Give me a FastAPI Todo Demo', 3, tempDir);
  assert.strictEqual(files.length, 3, 'should create 3 tasks');
  for (const f of files) {
    const json = JSON.parse(await fs.readFile(f, 'utf8'));
    assert.ok(json.id && json.module === 'demo');
  }
  console.log('dispatcher.autoPlan test passed');
})(); 