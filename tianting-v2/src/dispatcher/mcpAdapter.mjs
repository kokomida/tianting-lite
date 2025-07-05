/**
 * MCP Adapter for Sequential Thinking Integration
 * Connects with MCP SeqThinking server to generate task planning
 */

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

class MCPAdapter {
  constructor(mcpServerUrl = 'http://localhost:3001') {
    this.serverUrl = mcpServerUrl;
  }

  /**
   * Ask MCP SeqThinking server for sequential planning
   * @param {string} goal - The goal or requirement to plan for
   * @returns {Promise<Object[]>} Array of planning steps
   */
  async askSequential(goal) {
    try {
      const response = await fetch(`${this.serverUrl}/ask_sequential`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ goal })
      });

      if (!response.ok) {
        throw new Error(`MCP Server responded with status: ${response.status}`);
      }

      const data = await response.json();
      return data.steps || [];
    } catch (error) {
      console.error('Error calling MCP Server:', error);
      throw new Error(`Failed to get sequential planning: ${error.message}`);
    }
  }

  /**
   * Generate task drafts based on MCP sequential planning
   * @param {string} goal - The goal to plan for
   * @param {string} outputDir - Directory to write draft tasks
   * @returns {Promise<string>} Path to generated draft file
   */
  async generateTaskDrafts(goal, outputDir = 'tasks/generated') {
    // Get sequential steps from MCP
    const steps = await this.askSequential(goal);
    
    if (!steps || steps.length === 0) {
      throw new Error('No steps returned from MCP server');
    }

    // Ensure output directory exists
    const tasksOutputDir = path.resolve(outputDir);
    await fs.mkdir(tasksOutputDir, { recursive: true });

    // Generate timestamp-based filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = path.join(tasksOutputDir, `${timestamp}-draft.json`);

    // Convert MCP steps to task draft format
    const taskDrafts = steps.map((step, index) => {
      const taskId = `draft-${String(index + 1).padStart(2, '0')}`;
      
      return {
        id: taskId,
        role: this._inferRoleFromStep(step),
        objective: step.description || step.task || step.action || goal,
        implementation_guide: step.details || step.implementation || `Execute: ${step.description}`,
        success_criteria: step.success_criteria || step.acceptance || 'Task completed successfully',
        dependencies: index > 0 ? [`draft-${String(index).padStart(2, '0')}`] : [],
        required_stage: ['unit'],
        token_budget: 1500,
        status: 'pending',
        priority: step.priority || 'P2',
        tags: ['mcp-generated', 'draft'],
        created_at: new Date().toISOString(),
        mcp_source: {
          goal: goal,
          step_index: index,
          original_step: step
        }
      };
    });

    // Write draft tasks to file
    const draftData = {
      generated_at: new Date().toISOString(),
      source: 'mcp-seqthinking',
      goal: goal,
      total_tasks: taskDrafts.length,
      tasks: taskDrafts
    };

    await fs.writeFile(filename, JSON.stringify(draftData, null, 2), 'utf8');
    
    console.log(`Generated ${taskDrafts.length} task drafts: ${filename}`);
    return filename;
  }

  /**
   * Infer role from MCP step content
   * @param {Object} step - MCP planning step
   * @returns {string} Inferred role
   */
  _inferRoleFromStep(step) {
    const content = JSON.stringify(step).toLowerCase();
    
    if (content.includes('test') || content.includes('unittest') || content.includes('pytest')) {
      return 'qa-engineer';
    }
    if (content.includes('docker') || content.includes('deploy') || content.includes('ci/cd')) {
      return 'devops-engineer';
    }
    if (content.includes('frontend') || content.includes('ui') || content.includes('react') || content.includes('vue')) {
      return 'frontend-developer';
    }
    if (content.includes('backend') || content.includes('api') || content.includes('database') || content.includes('server')) {
      return 'python-backend-developer';
    }
    if (content.includes('document') || content.includes('readme') || content.includes('spec')) {
      return 'technical-writer';
    }
    
    // Default role
    return 'python-backend-developer';
  }

  /**
   * Health check for MCP server connection
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
      console.warn('MCP Server health check failed:', error.message);
      return false;
    }
  }
}

export { MCPAdapter };
export default MCPAdapter;