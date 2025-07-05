## Memory Management Fix for Windows CI

- CI still red due to missing `self._tag_index` and `db_path=":memory:"` logic in root `src/memoryhub/memory_manager.py`
- Windows still writing to temporary `memory.db`
- Previous rsync did not overwrite due to identical timestamps
- Root file remained on old version

### Fix Steps
- Checkout fix branch: `git checkout fix/win-handle`
- Open and modify `src/memoryhub/memory_manager.py`
- Add:
  - Import for `RoaringBitmapTagIndex`
  - Conditional `db_path` for Windows `:memory:`
  - Initialize `self._tag_index`
  - Add memory to tag index
  - Implement `recall_by_tags()` method
  - Clear tag index in `close()`
- Commit and push changes
- Wait for Linux and Windows CI tests to pass before merging