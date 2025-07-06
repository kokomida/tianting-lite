const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const fse = require('fs-extra');

// Helper function to get the session file path
const getSessionFilePath = (logDir) => path.join(logDir, '.tiangong-session.json');
const getRequestFilePath = (requestDir, timestamp) => path.join(requestDir, `request-${timestamp}.json`);

module.exports = {
  getDependencies() {
    return [
      'fs-extra@^11.1.0',
      'chokidar@^3.5.0'
    ];
  },

  getMetadata() {
    return {
      name: 'tiangong-orchestrator',
      description: 'AI开发团队项目经理 - 用于创建任务订单，并与神庭哨兵协作管理Claude Code任务。',
      version: '2.0.0',
      category: 'orchestration',
      author: '鲁班',
      tags: ['claude-code', 'wsl', 'orchestration', 'shenting']
    };
  },

  getSchema() {
    return {
        type: 'object',
        properties: {
            action: {
                type: 'string',
                enum: ['tiangong:start', 'tiangong:status', 'tiangong:stop'],
                description: '要执行的操作：start(创建任务订单), status(检查状态), stop(请求停止任务)'
            },
            tasks: {
                type: 'array',
                items: {
                    type: 'object',
                    properties: {
                        name: { type: 'string', description: '任务的唯一名称' },
                        command: { type: 'string', description: '要在WSL中执行的Claude Code命令' },
                        workdir: { type: 'string', description: 'WSL中的工作目录 (例如 /home/user/project)' }
                    },
                    required: ['name', 'command']
                },
                description: '任务列表，仅在 action 为 start 时需要'
            },
            logDir: {
                type: 'string',
                default: './tiangong-logs',
                description: '存储所有日志和会话文件的目录'
            },
            requestDir: {
                type: 'string',
                default: './tiangong-requests',
                description: '存放任务订单文件的目录'
            }
        },
        required: ['action', 'logDir']
    };
  },

  validate(params) {
    const errors = [];
    if (params.action === 'tiangong:start' && (!params.tasks || params.tasks.length === 0)) {
        errors.push("action 'tiangong:start' requires a non-empty 'tasks' array.");
    }
    return {
        valid: errors.length === 0,
        errors: errors
    };
  },

  async execute(params) {
    const { action, logDir, tasks, requestDir } = params;
    
    try {
        await fse.ensureDir(logDir);
        await fse.ensureDir(requestDir);
        
        switch (action) {
            case 'tiangong:start':
                return await this.createTaskRequest(tasks, logDir, requestDir);
            case 'tiangong:status':
                return await this.getTasksStatus(logDir);
            case 'tiangong:stop':
                 return await this.createStopRequest(logDir, requestDir);
            default:
                throw new Error(`Unknown action: ${action}`);
        }
    } catch (error) {
        return {
            success: false,
            error: {
                code: 'EXECUTION_ERROR',
                message: error.message,
                details: error.stack
            }
        };
    }
  },

  async createTaskRequest(tasks, logDir, requestDir) {
    const timestamp = Date.now();
    const requestFile = getRequestFilePath(requestDir, timestamp);
    const request = {
        type: 'START_TASKS',
        timestamp,
        payload: {
            tasks,
            logDir
        }
    };
    await fse.writeJson(requestFile, request, { spaces: 2 });
    return {
        success: true,
        data: {
            message: "Task creation order has been successfully placed.",
            requestFile: requestFile
        }
    };
  },

  async getTasksStatus(logDir) {
    const sessionFile = getSessionFilePath(logDir);
    if (!fse.existsSync(sessionFile)) {
        return { success: false, error: { code: 'NO_SESSION', message: 'No active session found. Has the Shenting sentry processed any tasks?' } };
    }
    const session = await fse.readJson(sessionFile);
    return { success: true, data: { tasks: session.tasks } };
  },

  async createStopRequest(logDir, requestDir) {
    const timestamp = Date.now();
    const requestFile = getRequestFilePath(requestDir, timestamp);
    const request = {
        type: 'STOP_ALL_TASKS',
        timestamp,
        payload: {
            logDir
        }
    };
     await fse.writeJson(requestFile, request, { spaces: 2 });
    return {
        success: true,
        data: {
            message: "A request to stop all tasks has been placed.",
            requestFile: requestFile
        }
    };
  }
}; 