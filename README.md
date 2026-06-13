# Folder Lock (secret-folder)

A simple cross-platform (Windows-focused) Python utility to lock and restore access to folders using OS ACLs and a small SQLite database to track locked paths with bcrypt-hashed passwords.

## Features

- Initialize a local SQLite database (`folder.db`) to track protected folders.
- Lock a folder by storing a bcrypt hash of a user-provided password and restricting access using Windows `icacls`.
- Restore access to a locked folder after verifying the password.

## Requirements

- Python 3.8+ recommended
- Windows (the `icacls` commands used are Windows-specific)
- Packages (can be installed with `pip`):
  - `bcrypt`
  - `termcolor`

Install dependencies:

```powershell
python -m pip install bcrypt termcolor
```

## Files

- `main.py`: CLI entrypoint. Commands: `init-db`, `lock`, `restore`.
- `database.py`: Creates `folder.db` and the `folders` table.
- `secret.py`: Interacts with the user to lock a folder and store a password hash.
- `verify.py`: Verifies a password and restores folder access.

## Usage

Initialize the database (first run):

```powershell
python main.py init-db
```

Lock a folder (will prompt for path and password):

```powershell
python main.py lock
```

Restore a folder (will prompt for path and password):

```powershell
python main.py restore
```

## Security notes

- Passwords are hashed with `bcrypt` before being stored in `folder.db`.
- The project stores password hashes and folder paths locally in `folder.db`.
- The ACL commands used (`icacls`) are Windows-specific and require appropriate permissions to run.
- This tool does not securely erase sensitive data (e.g., in-memory strings). Take care when using it on multi-user systems.

## Limitations & TODOs

- Non-Windows platforms are not supported for ACL changes; the code will need platform-specific handling for Linux/macOS (e.g., `chmod`, `setfacl`).
- Consider adding validation for folder paths and exception handling for subprocess calls.
- Consider adding the ability to remove records from the database after restoring.

## License

This project is provided as-is without warranty. Use at your own risk.
