# Vaultix / Secret Folder

A Windows-focused Python utility for protecting folders with password-based locking and restoring access using OS ACLs. The app stores encrypted passwords and folder metadata in a local SQLite database.

## Features

- CLI and GUI entrypoints:
  - CLI commands: `init-db`, `lock`, `restore`
  - GUI opens automatically if no CLI command is provided
- Local SQLite database `folder.db` stores folder paths, bcrypt password hashes, lock state, creation time, and update time
- Lock a folder by denying the current user full access via Windows `icacls`
- Restore folder access by granting the current user full control again
- View locked folder records and lock/unlock from the GUI

## Requirements

- Python 3.9+ recommended
- Windows
- Packages (install with `pip`):
  - `bcrypt`
  - `termcolor`
  - `PySide6`

Install dependencies:

```powershell
python -m pip install bcrypt termcolor PySide6
```

## Files

- `src/main.py`: entrypoint that dispatches CLI commands or launches the GUI
- `src/cli.py`: command-line command parser and dispatcher
- `src/database.py`: initializes `folder.db` and defines helper database access functions
- `src/secret.py`: prompts the user for folder path and password, hashes the password, stores the record, and locks the folder
- `src/verify.py`: verifies the password and restores folder access
- `src/gui.py`: Qt-based graphical interface for listing folders and locking/unlocking

## Usage

From the project root, use the `src/main.py` entrypoint.

Initialize the database:

```powershell
python src/main.py init-db
```

Open the GUI:

```powershell
python src/main.py
```

Force GUI mode explicitly:

```powershell
python src/main.py --gui
```

Lock a folder from the CLI:

```powershell
python src/main.py lock
```

Restore a locked folder from the CLI:

```powershell
python src/main.py restore
```

## How it works

- `init-db` creates `folder.db` and the `folders` table.
- `lock` prompts for a folder path and password, then stores a bcrypt hash and applies Windows ACL restrictions.
- `restore` prompts for the folder path and password, validates the hash, and restores ACL access.
- The GUI displays saved folders and lets you unlock or relock directly.

## Security notes

- Passwords are hashed with `bcrypt` before storage.
- The SQLite database stores folder paths, password hashes, and lock state locally.
- The locking mechanism is Windows-specific and depends on `icacls`.
- The app does not securely wipe passwords from memory.

## Limitations

- Only Windows ACL support is implemented.
- Non-Windows platforms are not supported.
- Records remain in the database after restore; the app marks folders as unlocked instead of deleting entries.
- The project may benefit from additional path validation and subprocess error handling.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

This software is provided "as is", without warranty of any kind. Use at your own risk.
