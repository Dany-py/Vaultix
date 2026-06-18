# Changelog

## [1.1.0] - 2025-06-17
### Added
- Password-protected folder locking for Windows
- Password hashing with `bcrypt`
- SQLite database storage of folder records
- `lock` command to restrict access with Windows `icacls`
- `restore` command to restore folder access
- Qt-based GUI for browsing stored folders and unlocking/relocking
- `init-db` command to initialize the local `folder.db`

### Changed
- CLI now dispatches to GUI when no command is provided
- Folder records now include lock state, creation time, and update time
- Restoring access updates the `is_locked` state instead of deleting records

### Known limitations
- Works only on Windows
- Requires appropriate permissions to use `icacls`

---
## [2.0.0] - Coming soon
### Planned
- Linux support
- macOS support