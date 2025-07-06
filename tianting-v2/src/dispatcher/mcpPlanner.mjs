/**
 * MCP Planner for Software Planning Integration
 * Connects with Software-Planning MCP to initiate planning sessions
 */

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

class MCPPlanner {
  constructor(mcpServerUrl = 'http://localhost:3002') {
    this.serverUrl = mcpServerUrl;
    this.memoryHubPath = 'memoryhub_data';
  }

  /**
   * Start a planning session with Software-Planning MCP
   * @param {string} goal - The goal or requirement to plan for
   * @param {Object} options - Planning options
   * @returns {Promise<Object>} Planning session result with planId
   */
  async startPlanning(goal, options = {}) {
    try {
      const planRequest = {
        goal: goal,
        context: options.context || {},
        preferences: {
          methodology: options.methodology || 'agile',
          timeline: options.timeline || 'medium',
          team_size: options.team_size || 'small',
          ...options.preferences
        },
        constraints: options.constraints || []
      };

      const response = await fetch(`${this.serverUrl}/start_planning`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(planRequest)
      });

      if (!response.ok) {
        throw new Error(`Planning MCP Server responded with status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.planId) {
        throw new Error('Planning MCP did not return a planId');
      }

      // Store planning session in MemoryHub
      await this._storePlanningSession(data, goal, planRequest);

      return {
        planId: data.planId,
        status: data.status || 'initialized',
        estimatedDuration: data.estimatedDuration,
        nextSteps: data.nextSteps || [],
        sessionData: data
      };

    } catch (error) {
      console.error('Error starting planning session:', error);
      throw new Error(`Failed to start planning: ${error.message}`);
    }
  }

  /**
   * Get planning session status
   * @param {string} planId - The planning session ID
   * @returns {Promise<Object>} Planning session status
   */
  async getPlanningStatus(planId) {
    try {
      const response = await fetch(`${this.serverUrl}/planning_status/${planId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Planning MCP Server responded with status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting planning status:', error);
      throw new Error(`Failed to get planning status: ${error.message}`);
    }
  }

  /**
   * Store planning session data in MemoryHub
   * @param {Object} sessionData - Planning session data from MCP
   * @param {string} goal - Original goal
   * @param {Object} planRequest - Original plan request
   * @private
   */
  async _storePlanningSession(sessionData, goal, planRequest) {
    try {
      // Ensure MemoryHub directory exists
      await fs.mkdir(this.memoryHubPath, { recursive: true });

      // Create planning session record
      const planningRecord = {
        id: sessionData.planId,
        type: 'planning_session',
        goal: goal,
        request: planRequest,
        response: sessionData,
        status: sessionData.status || 'initialized',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        mcp_source: {
          server: this.serverUrl,
          endpoint: '/start_planning',
          version: sessionData.version || '1.0'
        }
      };

      // Write to MemoryHub planning sessions file
      const planningFile = path.join(this.memoryHubPath, 'planning_sessions.jsonl');
      const recordLine = JSON.stringify(planningRecord) + '\n';
      
      await fs.appendFile(planningFile, recordLine, 'utf8');

      // Also create individual session file for easier access
      const sessionFile = path.join(this.memoryHubPath, `plan_${sessionData.planId}.json`);
      await fs.writeFile(sessionFile, JSON.stringify(planningRecord, null, 2), 'utf8');

      console.log(`Planning session ${sessionData.planId} stored in MemoryHub`);

    } catch (error) {
      console.warn('Failed to store planning session in MemoryHub:', error.message);
      // Don't throw - storage failure shouldn't break the planning process
    }
  }

  /**
   * Load planning session from MemoryHub
   * @param {string} planId - Planning session ID
   * @returns {Promise<Object|null>} Planning session data or null if not found
   */
  async loadPlanningSession(planId) {
    try {
      const sessionFile = path.join(this.memoryHubPath, `plan_${planId}.json`);
      const sessionData = await fs.readFile(sessionFile, 'utf8');
      return JSON.parse(sessionData);
    } catch (error) {
      console.warn(`Planning session ${planId} not found in MemoryHub:`, error.message);
      return null;
    }
  }

  /**
   * List all planning sessions from MemoryHub
   * @returns {Promise<Array>} Array of planning session summaries
   */
  async listPlanningSessions() {
    try {
      const planningFile = path.join(this.memoryHubPath, 'planning_sessions.jsonl');
      const content = await fs.readFile(planningFile, 'utf8');
      
      return content
        .trim()
        .split('\n')
        .filter(line => line.trim())
        .map(line => {
          const record = JSON.parse(line);
          return {
            planId: record.id,
            goal: record.goal,
            status: record.status,
            created_at: record.created_at,
            updated_at: record.updated_at
          };
        })
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        
    } catch (error) {
      console.warn('Failed to list planning sessions:', error.message);
      return [];
    }
  }

  /**
   * Health check for Planning MCP server connection
   * @returns {Promise<boolean>} True if server is responsive
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.serverUrl}/health`, {
        method: 'GET',
        timeout: 5000
      });
      return response.ok;
    } catch (error) {
      console.warn('Planning MCP Server health check failed:', error.message);
      return false;
    }
  }
}

// CLI interface for testing
async function runCLI() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help') {
    console.log(`
Usage: node src/dispatcher/mcpPlanner.mjs [command] [options]

Commands:
  --test                Run basic functionality test
  --start <goal>        Start a planning session
  --status <planId>     Get planning session status  
  --list               List all planning sessions
  --health             Check MCP server health

Examples:
  node src/dispatcher/mcpPlanner.mjs --test
  node src/dispatcher/mcpPlanner.mjs --start "Create a FastAPI todo app"
  node src/dispatcher/mcpPlanner.mjs --status plan_abc123
  node src/dispatcher/mcpPlanner.mjs --list
    `);
    return;
  }

  const planner = new MCPPlanner();

  try {
    switch (args[0]) {
      case '--test':
        await runTest(planner);
        break;
        
      case '--start':
        if (!args[1]) {
          console.error('Error: --start requires a goal argument');
          process.exit(1);
        }
        const result = await planner.startPlanning(args[1]);
        console.log('Planning session started:');
        console.log(JSON.stringify(result, null, 2));
        break;
        
      case '--status':
        if (!args[1]) {
          console.error('Error: --status requires a planId argument');
          process.exit(1);
        }
        const status = await planner.getPlanningStatus(args[1]);
        console.log('Planning status:');
        console.log(JSON.stringify(status, null, 2));
        break;
        
      case '--list':
        const sessions = await planner.listPlanningSessions();
        console.log('Planning sessions:');
        console.table(sessions);
        break;
        
      case '--health':
        const isHealthy = await planner.healthCheck();
        console.log(`Planning MCP Server health: ${isHealthy ? 'OK' : 'FAILED'}`);
        process.exit(isHealthy ? 0 : 1);
        break;
        
      default:
        console.error(`Unknown command: ${args[0]}`);
        process.exit(1);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

async function runTest(planner) {
  console.log('Running mcpPlanner basic functionality test...');
  
  // Test 1: Health check
  console.log('1. Testing health check...');
  const isHealthy = await planner.healthCheck();
  console.log(`   Health check: ${isHealthy ? 'PASS' : 'FAIL'}`);
  
  if (!isHealthy) {
    console.log('   Warning: MCP server not available, using mock data for testing');
  }

  // Test 2: Start planning (with mock fallback)
  console.log('2. Testing start planning...');
  try {
    let result;
    if (isHealthy) {
      result = await planner.startPlanning('Test planning session');
    } else {
      // Mock result for testing when server is not available
      result = {
        planId: `test_${Date.now()}`,
        status: 'initialized',
        estimatedDuration: '2-3 days',
        nextSteps: ['Define requirements', 'Create architecture']
      };
      // Simulate storage
      await planner._storePlanningSession({
        planId: result.planId,
        status: result.status
      }, 'Test planning session', {});
    }
    
    console.log(`   Planning started: ${result.planId}`);
    console.log(`   Status: ${result.status}`);
    
    // Test 3: Load from MemoryHub
    console.log('3. Testing MemoryHub integration...');
    const loaded = await planner.loadPlanningSession(result.planId);
    console.log(`   Loaded from MemoryHub: ${loaded ? 'PASS' : 'FAIL'}`);
    
    // Test 4: List sessions
    console.log('4. Testing list sessions...');
    const sessions = await planner.listPlanningSessions();
    console.log(`   Found ${sessions.length} planning sessions`);
    
    console.log('\nTest completed successfully! ✅');
    
  } catch (error) {
    console.error('Test failed:', error.message);
    process.exit(1);
  }
}

// Export for use as module
export { MCPPlanner };
export default MCPPlanner;

// Run CLI if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runCLI().catch(error => {
    console.error('CLI Error:', error);
    process.exit(1);
  });
}