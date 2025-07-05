# 踩坑记录 (Pitfalls & Lessons Learned)

> 本文档用于汇总 Tianting-Lite 项目在开发、测试、部署过程中遇到的典型问题及其解决 / 规避策略，避免团队重复踩坑。每次出现新问题或已有问题再次复现时，请立即在此补充或更新对应条目。

| # | 日期 | 模块 / 场景 | 现象 | 根因分析 | 解决方案 | 预防措施 |
|---|-------|-------------|-------|-----------|-----------|-----------|
| 1 | 2025-07-05 | GitHub 分支管理 | 同一功能出现多个命名不一致的分支 (`feat/…` vs `feature/…`)，PR 目标基分支搞错，CI 未触发 | 缺乏统一的分支 / PR 模板规范；协作者未同步最新策略 | 手动合并并关闭旧分支；重新建 `feat/core-03a-clean` 作为单一真源 | ① 制定并公布分支命名规范 (feat/…、fix/…、docs/…) ；② 在 PR 模板中双重校验目标分支；③ 周会回顾分支列表 |
| 2 | 2025-07-05 | CI – Windows Runner | `tests` 全绿但 Windows job 报 "file handle not closed"，导致 workflow 标红 | 临时文件 / 数据库连接在 Windows 环境未及时关闭，`pytest` 进程持有句柄 | 在测试代码中使用 `with tempfile.TemporaryDirectory()` 并确保 `manager.close()` 在上下文退出前调用 | ① 所有资源密集型对象实现 `close()` / `__exit__()`；② Windows  runner 上启用 `pytest --strict-resource-warnings` |
| 3 | 2025-07-05 | Packaging  & PYTHONPATH | `setup.py` 缺失包目录导致 `pip install -e .` 无法找到 `memoryhub`; GitHub Actions 失败 | `packages` 参数遗漏；导入时依赖隐式所在路径 | 修复 `setup.py`/`pyproject.toml`，显式列出 `src`；在 CI 中设置 `PYTHONPATH=$GITHUB_WORKSPACE/src` | ① 使用 `setuptools.find_packages('src')`; ② pre-commit hook 执行 `python -m pip install -e . && python -c "import memoryhub"` |
| 5 | 2025-07-05 | Windows Runner | `shutil.rmtree` 抛 `WinError 32` (文件占用) | 资源句柄在对象删除时未及时释放，GC 延迟 | 在测试中使用双重 `with`；调用 `manager.close()` 后 `gc.collect()` | ① 所有测试用例使用 `with LayeredMemoryManager(...)`；② 在 Windows CI 启用 `pytest --strict-resource-warnings` |
| 6 | 2025-07-05 | CI Path Mismatch | 根 `src/` 与 `tianting-v2/src/` 代码不一致，CI 仅加载根路径，导致 `_tag_index` 缺失单测失败 | 分支只改 v2 目录，忘同步根目录 | 1) 总是同时修改两处或只保留一个 authoritative 目录；2) 在 CI 设置 `PYTHONPATH=./src:./tianting-v2/src`；3) pre-commit 检查双路径 diff | ① 引入 rsync 同步脚本 `scripts/sync-memoryhub.sh`; ② Roadmap v0.3 任务：移除根 src 冗余 |

---

## 更新流程
1. **记录**：遇坑第一现场记录现象、日志及重现步骤。
2. **定位**：分析根因并在表格中补充。必要时附上 issue / PR 链接。
3. **验证**：解决后在本地 + CI 双重验证通过。
4. **预防**：提出可执行的方案（脚本 / 规范 / Hook），并在相关文档或脚本中落地。

> 🚩 若条目已无效或策略过时，更新 **解决方案** 与 **预防措施** 字段，并在 PR 描述注明「updatepitfall:#序号」。 