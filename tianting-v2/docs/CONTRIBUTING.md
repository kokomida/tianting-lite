<!-- status: done -->
# Contributing Guide

> 本文件定义 Tianting-v2 代码 & 文档贡献流程关键约定。请在提交 PR 前务必阅读。

## 1. 分支命名
- `feat/<scope>` 新功能
- `fix/<scope>` 修复
- `docs/<scope>` 文档
- `chore/<scope>` 杂项

## 2. Pull Request 规则
1. **CI 绿灯**：PR 必须通过 CI 才能 Merge。
2. **阻塞依赖**：若 PR 依赖前置任务 / PR，请在描述中注明：
   ```text
   Depends-On: #4  # core-03a-ci-green
   ```
   - CI 有脚本校验 `Depends-On` 的 PR 状态；未绿 → PR 自动标红。
3. **Draft / WIP**：
   - 前置任务未完成 → 必须以 Draft 状态提交，标题加 `WIP:` 前缀。
   - 仅当所有依赖 PR 通过并合并后，作者运行：
     ```bash
     gh pr ready <number>
     ```
     或在 GitHub UI 中点击 “Ready for review”。
4. **任务引用**：在描述中添加 `References: <task-id>`，多任务用换行分隔。
5. **Review 要求**：
   - 至少 1 位 reviewer（O3 或你）批准。
   - Reviewer 必须检查任务 ID 是否与实现一致、CI 是否全绿。

## 3. 代码风格
- Python: `black`, `isort`, `flake8` (line-length 100)。
- JS/TS: `prettier`, `eslint`。
- Commit message 遵循 Conventional Commits。

## 4. 提交流程小抄
```bash
# 1. 创建分支
git switch -c feat/core-03a-ci-green
# 2. 开发 & 本地测试
black src tests && isort src tests && flake8 src tests
pnpm test --workspaces
# 3. 提交 PR
gh pr create -t "feat(core-03a): CI 修绿" -b "References: core-03a-ci-green"
# 4. 若依赖其它 PR
# gh pr edit <number> --add-body "\nDepends-On: #4"
# 5. 等待 CI 绿 + Review
```

---
> 初版由 O3 生成：2025-07-06 