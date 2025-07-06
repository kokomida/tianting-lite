/**
 * Unit tests for MCP Planner Todo Synchronization
 */

import fs from 'fs/promises';
import path from 'path';
import assert from 'assert';
import { MCPPlanner } from '../src/dispatcher/mcpPlanner.mjs';

// Mock fetch for testing
global.fetch = async (url, options) => {
  const body = options?.body ? JSON.parse(options.body) : {};
  
  if (url.includes('/add_todo')) {
    // Mock add_todo response
    const todoItem = body;
    
    if (todoItem.title.includes('error')) {
      return {
        ok: false,
        status: 500
      };
    }
    
    if (todoItem.title.includes('no-id')) {
      return {
        ok: true,
        json: async () => ({
          status: 'created',
          message: 'Todo created but no ID returned'
        })
      };
    }
    
    // Normal successful response
    const todoId = `todo_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    return {
      ok: true,
      json: async () => ({
        todoId: todoId,
        status: 'created',
        title: todoItem.title,
        priority: todoItem.priority,
        tags: todoItem.tags
      })
    };
  }
  
  if (url.includes('/start_planning')) {
    // Mock start_planning response for setup
    const planId = `plan_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    return {
      ok: true,
      json: async () => ({
        planId: planId,
        status: 'initialized',
        estimatedDuration: '2-3 days',
        nextSteps: ['Define requirements', 'Create architecture']
      })
    };
  }
  
  if (url.includes('/health')) {
    return { ok: true };
  }
  
  throw new Error('Unknown endpoint');
};

(async () => {
  const testOutputDir = path.join('.tmp-test', 'todo-sync-output');
  
  // Clean up test directory
  await fs.rm(testOutputDir, { recursive: true, force: true });

  const planner = new MCPPlanner('http://localhost:3002');
  planner.memoryHubPath = testOutputDir;

  try {
    // Test setup: Create sample task drafts
    const sampleTaskDrafts = [
      {
        id: 'task_01',
        role: 'python-backend-developer',
        objective: 'Set up FastAPI project structure',
        implementation_guide: 'Create main.py, models, and basic project layout',
        success_criteria: 'Project structure created',
        priority: 'P1',
        tags: ['setup', 'backend'],
        dependencies: []
      },
      {
        id: 'task_02', 
        role: 'python-backend-developer',
        objective: 'Implement CRUD endpoints',
        implementation_guide: 'Create GET, POST, PUT, DELETE endpoints',
        success_criteria: 'All CRUD operations working',
        priority: 'P1',
        tags: ['api', 'backend'],
        dependencies: ['task_01']
      },
      {
        id: 'task_03',
        role: 'qa-engineer',
        objective: 'Write comprehensive tests',
        implementation_guide: 'Create pytest test suite with >80% coverage',
        success_criteria: 'Tests pass and coverage >= 80%',
        priority: 'P2',
        tags: ['testing'],
        dependencies: ['task_02']
      }
    ];

    // Test 1: addTodoItems should successfully process task drafts
    console.log('Test 1: addTodoItems basic functionality');
    const testPlanId = 'test_plan_123';
    const result = await planner.addTodoItems(testPlanId, sampleTaskDrafts);
    
    assert.strictEqual(result.planId, testPlanId, 'Should return correct planId');
    assert.strictEqual(result.totalTasks, 3, 'Should process all 3 tasks');
    assert.strictEqual(result.successful.length, 3, 'All tasks should be successful');
    assert.strictEqual(result.failed.length, 0, 'No tasks should fail');
    assert.strictEqual(result.summary.successCount, 3, 'Summary should show 3 successes');
    assert.strictEqual(result.summary.successRate, '100.0%', 'Success rate should be 100%');

    // Verify each successful todo item
    result.successful.forEach((item, index) => {
      assert.ok(item.todoId, 'Each item should have todoId');
      assert.ok(item.todoId.startsWith('todo_'), 'TodoId should have correct prefix');
      assert.strictEqual(item.taskId, sampleTaskDrafts[index].id, 'TaskId should match');
      assert.strictEqual(item.title, sampleTaskDrafts[index].objective, 'Title should match objective');
    });

    // Test 2: Todo sync results should be stored in MemoryHub
    console.log('Test 2: MemoryHub storage verification');
    
    // Check sync log file
    const syncLogFile = path.join(testOutputDir, 'todo_sync_log.jsonl');
    const logExists = await fs.access(syncLogFile).then(() => true).catch(() => false);
    assert.ok(logExists, 'Sync log file should exist');
    
    const logContent = await fs.readFile(syncLogFile, 'utf8');
    const logLines = logContent.trim().split('\n');
    assert.ok(logLines.length > 0, 'Sync log should have entries');
    
    const logEntry = JSON.parse(logLines[0]);
    assert.strictEqual(logEntry.type, 'todo_sync_result', 'Log entry should have correct type');
    assert.strictEqual(logEntry.planId, testPlanId, 'Log entry should have correct planId');

    // Check individual sync result file
    const syncFile = path.join(testOutputDir, `todo_sync_${testPlanId}.json`);
    const syncFileExists = await fs.access(syncFile).then(() => true).catch(() => false);
    assert.ok(syncFileExists, 'Individual sync file should exist');

    // Test 3: Error handling for empty task drafts
    console.log('Test 3: Error handling for empty task drafts');
    try {
      await planner.addTodoItems('test_plan', []);
      assert.fail('Should have thrown an error for empty array');
    } catch (error) {
      assert.ok(error.message.includes('non-empty array'), 'Should handle empty array');
    }

    try {
      await planner.addTodoItems('test_plan', null);
      assert.fail('Should have thrown an error for null');
    } catch (error) {
      assert.ok(error.message.includes('non-empty array'), 'Should handle null input');
    }

    // Test 4: Partial failure handling
    console.log('Test 4: Partial failure handling');
    const mixedTaskDrafts = [
      {
        id: 'task_success',
        objective: 'Successful task',
        implementation_guide: 'This will succeed',
        priority: 'P1'
      },
      {
        id: 'task_error',
        objective: 'error task',  // This will trigger mock error
        implementation_guide: 'This will fail',
        priority: 'P2'
      },
      {
        id: 'task_success2',
        objective: 'Another successful task',
        implementation_guide: 'This will also succeed',
        priority: 'P1'
      }
    ];

    const partialResult = await planner.addTodoItems('test_plan_partial', mixedTaskDrafts);
    
    assert.strictEqual(partialResult.totalTasks, 3, 'Should process all 3 tasks');
    assert.strictEqual(partialResult.successful.length, 2, 'Should have 2 successful tasks');
    assert.strictEqual(partialResult.failed.length, 1, 'Should have 1 failed task');
    assert.strictEqual(partialResult.summary.successRate, '66.7%', 'Success rate should be 66.7%');
    
    const failedTask = partialResult.failed[0];
    assert.strictEqual(failedTask.taskId, 'task_error', 'Failed task should be the error task');
    assert.ok(failedTask.error, 'Failed task should have error message');

    // Test 5: _convertTaskToTodoItem should generate correct format
    console.log('Test 5: Task to Todo item conversion');
    const testTask = {
      id: 'test_task',
      role: 'backend-developer',
      objective: 'Test objective',
      implementation_guide: 'Test implementation',
      success_criteria: 'Test criteria',
      priority: 'P1',
      tags: ['test', 'unit'],
      dependencies: ['dep1', 'dep2'],
      token_budget: 1500
    };

    const todoItem = planner._convertTaskToTodoItem(testTask, 'test_plan', 0);
    
    assert.strictEqual(todoItem.title, 'Test objective', 'Title should match objective');
    assert.strictEqual(todoItem.description, 'Test implementation', 'Description should match implementation_guide');
    assert.strictEqual(todoItem.priority, 'high', 'P1 should map to high priority');
    assert.ok(todoItem.tags.includes('mcp-planning'), 'Should include mcp-planning tag');
    assert.ok(todoItem.tags.includes('plan:test_plan'), 'Should include plan tag');
    assert.ok(todoItem.tags.includes('test'), 'Should include original tags');
    assert.strictEqual(todoItem.status, 'pending', 'Status should be pending');
    assert.ok(todoItem.due_date, 'Should have due date');
    
    const metadata = todoItem.metadata;
    assert.strictEqual(metadata.planId, 'test_plan', 'Metadata should include planId');
    assert.strictEqual(metadata.taskId, 'test_task', 'Metadata should include taskId');
    assert.strictEqual(metadata.role, 'backend-developer', 'Metadata should include role');
    assert.deepStrictEqual(metadata.dependencies, ['dep1', 'dep2'], 'Metadata should include dependencies');

    // Test 6: Priority mapping
    console.log('Test 6: Priority mapping');
    assert.strictEqual(planner._mapPriorityToTodoFormat('P1'), 'high', 'P1 should map to high');
    assert.strictEqual(planner._mapPriorityToTodoFormat('P2'), 'medium', 'P2 should map to medium');
    assert.strictEqual(planner._mapPriorityToTodoFormat('P3'), 'low', 'P3 should map to low');
    assert.strictEqual(planner._mapPriorityToTodoFormat('high'), 'high', 'high should stay high');
    assert.strictEqual(planner._mapPriorityToTodoFormat('unknown'), 'medium', 'Unknown should default to medium');

    // Test 7: Due date calculation
    console.log('Test 7: Due date calculation');
    const dueDateTask1 = { dependencies: [] };
    const dueDateTask2 = { dependencies: ['dep1', 'dep2'] };
    
    const dueDate1 = planner._calculateDueDate(dueDateTask1, 0);
    const dueDate2 = planner._calculateDueDate(dueDateTask2, 1);
    
    assert.ok(dueDate1, 'Should return due date for task without dependencies');
    assert.ok(dueDate2, 'Should return due date for task with dependencies');
    assert.ok(new Date(dueDate2) > new Date(dueDate1), 'Task with dependencies should have later due date');

    // Test 8: syncTaskDraftsToTodo integration test
    console.log('Test 8: syncTaskDraftsToTodo integration');
    
    // First create a planning session with associated task drafts
    const planResult = await planner.startPlanning('Integration test project');
    const integrationPlanId = planResult.planId;
    
    // Create a tasks/generated directory and draft file
    const tasksDir = path.join(process.cwd(), 'tasks', 'generated');
    await fs.mkdir(tasksDir, { recursive: true });
    
    const draftData = {
      generated_at: new Date().toISOString(),
      source: 'test-integration',
      goal: 'Integration test project',
      total_tasks: 2,
      tasks: [
        {
          id: 'integration_task_01',
          objective: 'Integration test task 1',
          implementation_guide: 'Test implementation 1',
          priority: 'P1',
          tags: [`plan:${integrationPlanId}`],
          mcp_source: { planId: integrationPlanId }
        },
        {
          id: 'integration_task_02', 
          objective: 'Integration test task 2',
          implementation_guide: 'Test implementation 2',
          priority: 'P2',
          tags: [`plan:${integrationPlanId}`],
          mcp_source: { planId: integrationPlanId }
        }
      ]
    };
    
    const draftFile = path.join(tasksDir, `${integrationPlanId}-draft.json`);
    await fs.writeFile(draftFile, JSON.stringify(draftData, null, 2));
    
    // Test syncTaskDraftsToTodo
    const syncIntegrationResult = await planner.syncTaskDraftsToTodo(integrationPlanId);
    
    assert.strictEqual(syncIntegrationResult.planId, integrationPlanId, 'Sync should use correct planId');
    assert.strictEqual(syncIntegrationResult.totalTasks, 2, 'Should sync 2 tasks');
    assert.strictEqual(syncIntegrationResult.successful.length, 2, 'Both tasks should succeed');
    
    // Clean up test file
    await fs.rm(draftFile).catch(() => {});

    // Test 9: Error handling for non-existent planning session
    console.log('Test 9: Error handling for non-existent planning session');
    try {
      await planner.syncTaskDraftsToTodo('non_existent_plan');
      assert.fail('Should have thrown an error for non-existent plan');
    } catch (error) {
      assert.ok(error.message.includes('not found'), 'Should handle non-existent planning session');
    }

    console.log('dispatcher.todoSync test passed - All tests successful! ✅');

  } catch (error) {
    console.error('Test failed:', error);
    process.exit(1);
  } finally {
    // Clean up test directory
    await fs.rm(testOutputDir, { recursive: true, force: true });
    
    // Clean up any test files in tasks/generated
    try {
      const tasksDir = path.join(process.cwd(), 'tasks', 'generated');
      const files = await fs.readdir(tasksDir).catch(() => []);
      for (const file of files) {
        if (file.includes('plan_') && file.endsWith('-draft.json')) {
          await fs.rm(path.join(tasksDir, file)).catch(() => {});
        }
      }
    } catch (e) {
      // Ignore cleanup errors
    }
  }
})();