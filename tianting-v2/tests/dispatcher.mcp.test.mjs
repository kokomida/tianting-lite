/**
 * Unit tests for MCP Adapter
 */

import fs from 'fs/promises';
import path from 'path';
import assert from 'assert';
import { MCPAdapter } from '../src/dispatcher/mcpAdapter.mjs';

// Mock fetch for testing
global.fetch = async (url, options) => {
  const body = JSON.parse(options.body || '{}');
  
  if (url.includes('/ask_sequential')) {
    // Mock MCP response based on goal
    const goal = body.goal;
    
    if (goal.includes('fastapi todo')) {
      return {
        ok: true,
        json: async () => ({
          steps: [
            {
              description: 'Set up FastAPI project structure',
              details: 'Create main.py, models, and basic project layout',
              success_criteria: 'Project structure created',
              priority: 'P1'
            },
            {
              description: 'Implement CRUD endpoints for todos',
              details: 'Create GET, POST, PUT, DELETE endpoints for todo management',
              success_criteria: 'All CRUD operations working',
              priority: 'P1'
            },
            {
              description: 'Write comprehensive tests',
              details: 'Create pytest test suite with >80% coverage',
              success_criteria: 'Tests pass and coverage >= 80%',
              priority: 'P2'
            },
            {
              description: 'Add Docker deployment',
              details: 'Create Dockerfile and docker-compose.yml',
              success_criteria: 'Container runs successfully',
              priority: 'P2'
            }
          ]
        })
      };
    }
    
    if (goal.includes('error')) {
      return {
        ok: false,
        status: 500
      };
    }
    
    // Default empty response
    return {
      ok: true,
      json: async () => ({ steps: [] })
    };
  }
  
  if (url.includes('/health')) {
    return { ok: true };
  }
  
  throw new Error('Unknown endpoint');
};

(async () => {
  const testOutputDir = path.join('.tmp-test', 'mcp-output');
  
  // Clean up test directory
  await fs.rm(testOutputDir, { recursive: true, force: true });

  const adapter = new MCPAdapter('http://localhost:3001');

  try {
    // Test 1: askSequential should return steps for valid goal
    const steps = await adapter.askSequential('fastapi todo app');
    assert.ok(Array.isArray(steps), 'Steps should be an array');
    assert.ok(steps.length > 0, 'Should return steps');
    assert.ok(steps[0].description, 'First step should have description');

    // Test 2: askSequential should handle server errors
    try {
      await adapter.askSequential('error case');
      assert.fail('Should have thrown an error');
    } catch (error) {
      assert.ok(error.message.includes('Failed to get sequential planning'), 'Should handle server errors');
    }

    // Test 3: askSequential should return empty array for no steps
    const emptySteps = await adapter.askSequential('empty goal');
    assert.ok(Array.isArray(emptySteps), 'Empty steps should be an array');
    assert.strictEqual(emptySteps.length, 0, 'Should return empty array');

    // Test 4: generateTaskDrafts should generate draft tasks file with correct structure
    const filename = await adapter.generateTaskDrafts('fastapi todo app', testOutputDir);
    
    // Verify file exists
    assert.ok(filename.includes(testOutputDir), 'Filename should include output directory');
    assert.ok(filename.includes('-draft.json'), 'Filename should include draft suffix');
    
    const fileExists = await fs.access(filename).then(() => true).catch(() => false);
    assert.ok(fileExists, 'File should exist');
    
    // Verify file content
    const content = await fs.readFile(filename, 'utf8');
    const data = JSON.parse(content);
    
    assert.ok(data.generated_at, 'Should have generated_at timestamp');
    assert.strictEqual(data.source, 'mcp-seqthinking', 'Should have correct source');
    assert.strictEqual(data.goal, 'fastapi todo app', 'Should have correct goal');
    assert.ok(data.total_tasks, 'Should have total_tasks count');
    assert.ok(Array.isArray(data.tasks), 'Tasks should be an array');
    assert.ok(data.tasks.length > 0, 'Should have tasks');
    
    // Verify task structure
    const task = data.tasks[0];
    assert.ok(task.id, 'Task should have id');
    assert.ok(task.role, 'Task should have role');
    assert.ok(task.objective, 'Task should have objective');
    assert.ok(task.implementation_guide, 'Task should have implementation_guide');
    assert.ok(task.success_criteria, 'Task should have success_criteria');
    assert.ok(Array.isArray(task.dependencies), 'Dependencies should be an array');
    assert.ok(Array.isArray(task.required_stage), 'Required_stage should be an array');
    assert.ok(task.token_budget, 'Task should have token_budget');
    assert.strictEqual(task.status, 'pending', 'Task status should be pending');
    assert.ok(task.priority, 'Task should have priority');
    assert.ok(Array.isArray(task.tags), 'Tags should be an array');
    assert.ok(task.created_at, 'Task should have created_at');
    assert.ok(task.mcp_source, 'Task should have mcp_source');
    
    assert.ok(task.tags.includes('mcp-generated'), 'Should include mcp-generated tag');
    assert.ok(task.tags.includes('draft'), 'Should include draft tag');

    // Test 5: should handle goals with no steps
    try {
      await adapter.generateTaskDrafts('empty goal', testOutputDir);
      assert.fail('Should have thrown an error for empty goal');
    } catch (error) {
      assert.ok(error.message.includes('No steps returned from MCP server'), 'Should handle empty steps');
    }

    // Test 6: _inferRoleFromStep should infer correct roles
    const testCases = [
      { step: { description: 'write pytest tests' }, expected: 'qa-engineer' },
      { step: { description: 'create Docker deployment' }, expected: 'devops-engineer' },
      { step: { description: 'build React frontend' }, expected: 'frontend-developer' },
      { step: { description: 'implement API backend' }, expected: 'python-backend-developer' },
      { step: { description: 'write documentation' }, expected: 'technical-writer' },
      { step: { description: 'general task' }, expected: 'python-backend-developer' }
    ];

    testCases.forEach(({ step, expected }) => {
      const role = adapter._inferRoleFromStep(step);
      assert.strictEqual(role, expected, `Should infer ${expected} for ${step.description}`);
    });

    // Test 7: healthCheck should return true for healthy server
    const isHealthy = await adapter.healthCheck();
    assert.strictEqual(isHealthy, true, 'Health check should return true');

    console.log('dispatcher.mcp test passed - All tests successful!');

  } catch (error) {
    console.error('Test failed:', error);
    process.exit(1);
  } finally {
    // Clean up test directory
    await fs.rm(testOutputDir, { recursive: true, force: true });
  }
})();