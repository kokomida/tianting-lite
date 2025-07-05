#!/usr/bin/env bash
# guard-prod-path.sh  阻止修改 production 目录文件
# 输入：PreToolUse JSON，经 stdin 传入

read -r payload
# 提取命令字段（兼容 Bash/Git 工具输入格式）
cmd=$(echo "$payload" | jq -r '.tool_input.command // ""')

if [[ "$cmd" == *"tianting-v2/production/"* ]]; then
  echo "禁止直接修改 tianting-v2/production/ 目录。请走发布流程。" >&2
  exit 2  # 阻止工具调用
fi

exit 0 