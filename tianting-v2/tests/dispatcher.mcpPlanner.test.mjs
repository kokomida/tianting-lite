/**
 * Unit tests for MCP Planner
 */

import fs from 'fs/promises';
import path from 'path';
import assert from 'assert';
import { MCPPlanner } from '../src/dispatcher/mcpPlanner.mjs';

// Mock fetch for testing
global.fetch = async (url, options) => {
  const body = options?.body ? JSON.parse(options.body) : {};
  
  if (url.includes('/start_planning')) {
    // Mock start_planning response
    const goal = body.goal;
    
    if (goal.includes('error')) {
      return {
        ok: false,
        status: 500
      };
    }
    
    if (goal.includes('no-plan-id')) {
      return {
        ok: true,
        json: async () => ({
          status: 'error',
          message: 'Failed to create plan'
        })
      };
    }
    
    // Normal successful response
    const planId = `plan_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    return {
      ok: true,
      json: async () => ({
        planId: planId,
        status: 'initialized',
        estimatedDuration: '2-3 days',
        nextSteps: [
          'Define detailed requirements',
          'Create system architecture',
          'Plan development sprints'
        ],
        version: '1.0',
        methodology: body.preferences?.methodology || 'agile'
      })
    };
  }
  
  if (url.includes('/planning_status/')) {
    const planId = url.split('/').pop();
    
    if (planId === 'invalid_plan') {
      return {
        ok: false,
        status: 404
      };
    }
    
    return {
      ok: true,
      json: async () => ({
        planId: planId,
        status: 'in_progress',
        progress: 0.3,
        currentPhase: 'requirements_analysis',
        nextSteps: ['Complete requirements', 'Begin architecture']
      })
    };
  }
  
  if (url.includes('/health')) {
    return { ok: true };
  }
  
  throw new Error('Unknown endpoint');
};

(async () => {
  const testOutputDir = path.join('.tmp-test', 'planner-output');
  
  // Clean up test directory
  await fs.rm(testOutputDir, { recursive: true, force: true });

  const planner = new MCPPlanner('http://localhost:3002');
  planner.memoryHubPath = testOutputDir;

  try {
    // Test 1: startPlanning should return planId and store in MemoryHub
    console.log('Test 1: startPlanning basic functionality');
    const result = await planner.startPlanning('Create a React dashboard app');
    
    assert.ok(result.planId, 'Should return planId');
    assert.ok(result.planId.startsWith('plan_'), 'PlanId should have correct prefix');
    assert.strictEqual(result.status, 'initialized', 'Should have initialized status');
    assert.ok(result.estimatedDuration, 'Should have estimated duration');
    assert.ok(Array.isArray(result.nextSteps), 'Should have nextSteps array');
    assert.ok(result.nextSteps.length > 0, 'Should have at least one next step');

    // Test 2: Planning session should be stored in MemoryHub
    console.log('Test 2: MemoryHub storage verification');
    const loadedSession = await planner.loadPlanningSession(result.planId);
    
    assert.ok(loadedSession, 'Session should be stored in MemoryHub');
    assert.strictEqual(loadedSession.id, result.planId, 'Stored planId should match');
    assert.strictEqual(loadedSession.type, 'planning_session', 'Should have correct type');
    assert.strictEqual(loadedSession.goal, 'Create a React dashboard app', 'Should store original goal');
    assert.ok(loadedSession.created_at, 'Should have created_at timestamp');
    assert.ok(loadedSession.mcp_source, 'Should have mcp_source metadata');

    // Test 3: Planning sessions list should include our session
    console.log('Test 3: listPlanningSessions functionality');
    const sessions = await planner.listPlanningSessions();
    
    assert.ok(Array.isArray(sessions), 'Should return array');
    assert.ok(sessions.length > 0, 'Should have at least one session');
    
    const ourSession = sessions.find(s => s.planId === result.planId);
    assert.ok(ourSession, 'Should find our planning session in list');
    assert.strictEqual(ourSession.goal, 'Create a React dashboard app', 'Listed session should have correct goal');

    // Test 4: getPlanningStatus should work with valid planId
    console.log('Test 4: getPlanningStatus functionality');
    const status = await planner.getPlanningStatus(result.planId);
    
    assert.ok(status.planId, 'Status should have planId');
    assert.ok(status.status, 'Status should have status field');
    assert.ok(status.currentPhase, 'Status should have currentPhase');

    // Test 5: Error handling for server errors
    console.log('Test 5: Error handling for server errors');
    try {
      await planner.startPlanning('error case');
      assert.fail('Should have thrown an error');
    } catch (error) {
      assert.ok(error.message.includes('Failed to start planning'), 'Should handle server errors');
    }

    // Test 6: Error handling for missing planId in response
    console.log('Test 6: Error handling for missing planId');
    try {
      await planner.startPlanning('no-plan-id case');
      assert.fail('Should have thrown an error');
    } catch (error) {
      assert.ok(error.message.includes('did not return a planId'), 'Should handle missing planId');
    }

    // Test 7: Error handling for invalid planId in status check
    console.log('Test 7: Error handling for invalid planId in status');
    try {
      await planner.getPlanningStatus('invalid_plan');
      assert.fail('Should have thrown an error');
    } catch (error) {
      assert.ok(error.message.includes('Failed to get planning status'), 'Should handle invalid planId');
    }

    // Test 8: startPlanning with custom options
    console.log('Test 8: startPlanning with custom options');
    const customResult = await planner.startPlanning('Build API server', {
      methodology: 'waterfall',
      timeline: 'long',
      team_size: 'large',
      context: { existing_systems: ['auth_service', 'db_cluster'] },
      constraints: ['budget_limit', 'legacy_compatibility']
    });
    
    assert.ok(customResult.planId, 'Should return planId for custom options');
    assert.strictEqual(customResult.status, 'initialized', 'Should have correct status');

    // Verify custom options were stored
    const customSession = await planner.loadPlanningSession(customResult.planId);
    assert.strictEqual(customSession.request.preferences.methodology, 'waterfall', 'Should store custom methodology');
    assert.strictEqual(customSession.request.preferences.timeline, 'long', 'Should store custom timeline');
    assert.ok(customSession.request.context, 'Should store context');
    assert.ok(Array.isArray(customSession.request.constraints), 'Should store constraints');

    // Test 9: healthCheck should return boolean
    console.log('Test 9: healthCheck functionality');
    const isHealthy = await planner.healthCheck();
    assert.strictEqual(typeof isHealthy, 'boolean', 'Health check should return boolean');

    // Test 10: loadPlanningSession should return null for non-existent session
    console.log('Test 10: loadPlanningSession for non-existent session');
    const nonExistent = await planner.loadPlanningSession('non_existent_plan');
    assert.strictEqual(nonExistent, null, 'Should return null for non-existent session');

    console.log('dispatcher.mcpPlanner test passed - All tests successful! ✅');

  } catch (error) {
    console.error('Test failed:', error);
    process.exit(1);
  } finally {
    // Clean up test directory
    await fs.rm(testOutputDir, { recursive: true, force: true });
  }
})();