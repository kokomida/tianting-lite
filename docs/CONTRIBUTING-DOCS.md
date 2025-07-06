<!-- status: draft -->
# Documentation Contribution Guide (CONTRIBUTING-DOCS)

> 本指南适用于 **Tianting-Lite** 所有文档贡献者，涵盖章节排布、命名规则、Lint 校验、PR 流程与版本管理规范。请在提交任何文档修改前通读全文。

---

## 1. 章节结构 & 命名
| 章节号 | 文件 | 说明 |
|--------|------|------|
| 00-10 | `docs/<num>-<name>.md` | 产品主文档，编号固定，禁止删除或更改顺序 |
| 11+   | `docs/<num>-<name>.md` | 补充文档，可按需新建，但须在 `docs/index.md` 更新导航 |
| Templates | `docs/templates/` | 协议、角色、脚手架模板 |
| Glossary | `docs/11-glossary.md` | 术语表，使用 `| term | definition |` 表格格式 |
| Knowledge | `docs/knowledge/YYYY/MM/DD/*.md` | 概念卡片，遵循日期路径方便索引 |

命名风格：文件与标题使用 **kebab-case**，英文小写，数字两位填充 (`05-detailed-design.md`)。

---

## 2. 顶部元数据 (Front-Matter-Lite)
每个 Markdown 顶部必须包含以下 HTML 注释形式元数据：
```markdown
<!-- status: draft|in_progress|done|todo -->
```
状态含义：
- `draft`: 草稿，不要求格式完整；CI 仅做 Markdown lint。
- `in_progress`: 主要内容完成 ≥50%；CI 执行 lint + 引用检查。
- `done`: 内容冻结，需通过全文校验脚本 (`lint-doc-status.mjs`)。
- `todo`: 仅标题与占位符，排期中。

> **CI Gate**：`done` 级文档若被修改，必须在 PR 描述说明原因并更新 `CHANGELOG.md`。

---

## 3. 内容风格
1. **中文为主，夹带英语专业词可保留原文**。
2. 行宽 ≤ 100 字符，便于 diff 与侧边翻译。
3. 一级标题 `#` 只出现一次，其余使用 `## / ###`。
4. 表格首列左对齐；数值列右对齐；标题行用 `|----|` 分隔。
5. 代码块需声明语言：```bash / ```json / ```mermaid。
6. 图片统一放 `PromptX/assets/` 或 `tianting-v2/docs/assets/`，引用相对路径。

---

## 4. 校验脚本 & CI
| 脚本 | 作用 | 触发 |
|-------|------|------|
| `scripts/generate-doc-index.mjs` | 自动更新 `docs/index.md` | pre-commit & CI |
| `scripts/lint-doc-status.mjs` | 检查 `status` 标签与格式 | pre-commit & CI |
| `scripts/lint-oes.mjs` | AJV 校验 `*.task.json` | pre-commit & CI |
| `scripts/lint-learning-schema.mjs` | 校验 Explainer 输出 Schema | CI nightly |

CI 失败时请先本地运行对应脚本排错后再推送。

---

## 5. Pull Request 流程
1. **从 `main` 切分分支**，命名 `docs/<topic>-<yyMMdd>`。
2. 完成修改后，本地执行 `pnpm docs:lint`（别名执行全部脚本）。
3. 填写 PR 模板：
   - **What & Why**：修改内容、动机。
   - **Related Issue / TODO**：若关联请贴链接。
   - **Checklist**：勾选脚本通过、`CHANGELOG.md` 更新。
4. 至少 1 名 Reviewer 通过后合并；若影响 CI/CD，需 DevOps 额外审批。

---

## 6. 版本管理
- 任何 **用户可见** 文档变更须追加到 `docs/CHANGELOG.md`，按日期倒序。
- 大改动 (重命名/拆分) 须在 PR 中附 **迁移指北** 描述旧链接跳转。
- *禁止* 修改历史记录：若需撤销，请新 PR 反向更改并说明。

---

## 7. 常见问题
| 问题 | 解决方案 |
|------|-----------|
| CI 提示 `Missing status tag` | 在文件顶部添加 `<!-- status: ... -->` |
| Mermaid 渲染失败 | 在 PR 中贴图；检查节点名称是否含空格或特殊字符 |
| AJV schema 校验 Error | 对照 `docs/06-oes-spec.md` 修正字段 |

---

> 最后更新：2025-07-06 – Maintained by AI PM & Docs Team 