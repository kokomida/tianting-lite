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
   * Add tasks to MCP Todo system
   * @param {string} planId - Planning session ID
   * @param {Array} taskDrafts - Array of task draft objects
   * @returns {Promise<Object>} Result of todo synchronization
   */
  async addTodoItems(planId, taskDrafts) {
    try {
      if (!Array.isArray(taskDrafts) || taskDrafts.length === 0) {
        throw new Error('taskDrafts must be a non-empty array');
      }

      const results = {
        planId: planId,
        totalTasks: taskDrafts.length,
        successful: [],
        failed: [],
        summary: {}
      };

      // Process each task draft
      for (const [index, task] of taskDrafts.entries()) {
        try {
          const todoItem = this._convertTaskToTodoItem(task, planId, index);
          const response = await fetch(`${this.serverUrl}/add_todo`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(todoItem)
          });

          if (!response.ok) {
            throw new Error(`MCP Server responded with status: ${response.status}`);
          }

          const result = await response.json();
          results.successful.push({
            taskId: task.id || `task_${index}`,
            todoId: result.todoId || result.id,
            title: task.objective || task.title || 'Untitled task'
          });

        } catch (error) {
          console.error(`Failed to add todo item for task ${task.id || index}:`, error.message);
          results.failed.push({
            taskId: task.id || `task_${index}`,
            title: task.objective || task.title || 'Untitled task',
            error: error.message
          });
        }
      }

      // Update summary
      results.summary = {
        successCount: results.successful.length,
        failureCount: results.failed.length,
        successRate: (results.successful.length / results.totalTasks * 100).toFixed(1) + '%'
      };

      // Store todo sync results in MemoryHub
      await this._storeTodoSyncResults(results);

      console.log(`Todo sync completed: ${results.summary.successCount}/${results.totalTasks} successful`);
      
      return results;

    } catch (error) {
      console.error('Error adding todo items:', error);
      throw new Error(`Failed to add todo items: ${error.message}`);
    }
  }

  /**
   * Sync task drafts from a planning session to MCP Todo system
   * @param {string} planId - Planning session ID
   * @returns {Promise<Object>} Result of synchronization
   */
  async syncTaskDraftsToTodo(planId) {
    try {
      // Load planning session from MemoryHub
      const planningSession = await this.loadPlanningSession(planId);
      if (!planningSession) {
        throw new Error(`Planning session ${planId} not found`);
      }

      // Look for task drafts associated with this planning session
      // First check if there are drafts in the session data
      let taskDrafts = [];
      
      if (planningSession.response && planningSession.response.taskDrafts) {
        taskDrafts = planningSession.response.taskDrafts;
      } else {
        // Look for draft files that might be associated with this plan
        taskDrafts = await this._findAssociatedTaskDrafts(planId);
      }

      if (taskDrafts.length === 0) {
        throw new Error(`No task drafts found for planning session ${planId}`);
      }

      return await this.addTodoItems(planId, taskDrafts);

    } catch (error) {
      console.error('Error syncing task drafts to todo:', error);
      throw new Error(`Failed to sync task drafts: ${error.message}`);
    }
  }

  /**
   * Convert a task draft to MCP Todo item format
   * @param {Object} task - Task draft object
   * @param {string} planId - Planning session ID
   * @param {number} index - Task index
   * @returns {Object} Todo item in MCP format
   * @private
   */
  _convertTaskToTodoItem(task, planId, index) {
    return {
      title: task.objective || task.title || `Task ${index + 1}`,
      description: task.implementation_guide || task.description || '',
      priority: this._mapPriorityToTodoFormat(task.priority),
      tags: [
        'mcp-planning',
        `plan:${planId}`,
        ...(task.tags || []),
        task.role || 'general'
      ],
      metadata: {
        planId: planId,
        taskId: task.id,
        role: task.role,
        success_criteria: task.success_criteria,
        dependencies: task.dependencies || [],
        token_budget: task.token_budget,
        created_from: 'mcp-planner',
        original_task: task
      },
      due_date: this._calculateDueDate(task, index),
      status: 'pending'
    };
  }

  /**
   * Map task priority to MCP Todo format
   * @param {string} priority - Task priority (P1, P2, etc.)
   * @returns {string} Todo priority format
   * @private
   */
  _mapPriorityToTodoFormat(priority) {
    const priorityMap = {
      'P1': 'high',
      'P2': 'medium', 
      'P3': 'low',
      'high': 'high',
      'medium': 'medium',
      'low': 'low'
    };
    return priorityMap[priority] || 'medium';
  }

  /**
   * Calculate due date for a task based on dependencies and sequence
   * @param {Object} task - Task object
   * @param {number} index - Task index in sequence
   * @returns {string|null} ISO date string or null
   * @private
   */
  _calculateDueDate(task, index) {
    // Simple heuristic: each task gets 2 days, with dependencies adding delay
    const baseDays = 2;
    const dependencyDelay = (task.dependencies?.length || 0) * 1;
    const sequenceDelay = index * 1; // Later tasks get more time
    
    const totalDays = baseDays + dependencyDelay + sequenceDelay;
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + totalDays);
    
    return dueDate.toISOString();
  }

  /**
   * Find task drafts associated with a planning session
   * @param {string} planId - Planning session ID
   * @returns {Promise<Array>} Array of task drafts
   * @private
   */
  async _findAssociatedTaskDrafts(planId) {
    try {
      // Look in tasks/generated/ for draft files that might be associated
      const tasksGeneratedDir = path.join(process.cwd(), 'tasks', 'generated');
      
      try {
        const files = await fs.readdir(tasksGeneratedDir);
        const draftFiles = files.filter(f => f.endsWith('-draft.json'));
        
        for (const file of draftFiles) {
          const filePath = path.join(tasksGeneratedDir, file);
          const content = await fs.readFile(filePath, 'utf8');
          const draftData = JSON.parse(content);
          
          // Check if any tasks in this draft file reference our planId
          if (draftData.tasks && Array.isArray(draftData.tasks)) {
            const associatedTasks = draftData.tasks.filter(task => 
              task.mcp_source?.planId === planId ||
              task.tags?.includes(`plan:${planId}`)
            );
            if (associatedTasks.length > 0) {
              return associatedTasks;
            }
          }
        }
      } catch (dirError) {
        console.warn('Could not read tasks/generated directory:', dirError.message);
      }
      
      return [];
    } catch (error) {
      console.warn('Error finding associated task drafts:', error.message);
      return [];
    }
  }

  /**
   * Store todo synchronization results in MemoryHub
   * @param {Object} results - Sync results
   * @private
   */
  async _storeTodoSyncResults(results) {
    try {
      await fs.mkdir(this.memoryHubPath, { recursive: true });

      const syncRecord = {
        type: 'todo_sync_result',
        planId: results.planId,
        results: results,
        synced_at: new Date().toISOString(),
        mcp_source: {
          server: this.serverUrl,
          endpoint: '/add_todo'
        }
      };

      // Append to todo sync log
      const syncLogFile = path.join(this.memoryHubPath, 'todo_sync_log.jsonl');
      const recordLine = JSON.stringify(syncRecord) + '\n';
      await fs.appendFile(syncLogFile, recordLine, 'utf8');

      // Also create individual sync result file
      const syncFile = path.join(this.memoryHubPath, `todo_sync_${results.planId}.json`);
      await fs.writeFile(syncFile, JSON.stringify(syncRecord, null, 2), 'utf8');

    } catch (error) {
      console.warn('Failed to store todo sync results:', error.message);
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
  --sync-todos <planId> Sync task drafts to MCP Todo system
  --add-todos <planId> <draftsFile>  Add specific task drafts to MCP Todo

Examples:
  node src/dispatcher/mcpPlanner.mjs --test
  node src/dispatcher/mcpPlanner.mjs --start "Create a FastAPI todo app"
  node src/dispatcher/mcpPlanner.mjs --status plan_abc123
  node src/dispatcher/mcpPlanner.mjs --list
  node src/dispatcher/mcpPlanner.mjs --sync-todos plan_abc123
  node src/dispatcher/mcpPlanner.mjs --add-todos plan_abc123 ./tasks/generated/draft.json
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

      case '--sync-todos':
        if (!args[1]) {
          console.error('Error: --sync-todos requires a planId argument');
          process.exit(1);
        }
        const syncResult = await planner.syncTaskDraftsToTodo(args[1]);
        console.log('Todo sync result:');
        console.log(JSON.stringify(syncResult, null, 2));
        break;

      case '--add-todos':
        if (!args[1] || !args[2]) {
          console.error('Error: --add-todos requires planId and draftsFile arguments');
          process.exit(1);
        }
        const draftsContent = await fs.readFile(args[2], 'utf8');
        const draftsData = JSON.parse(draftsContent);
        const taskDrafts = Array.isArray(draftsData) ? draftsData : draftsData.tasks || [];
        
        const addResult = await planner.addTodoItems(args[1], taskDrafts);
        console.log('Add todos result:');
        console.log(JSON.stringify(addResult, null, 2));
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