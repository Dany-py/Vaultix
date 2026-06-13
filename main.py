import argparse
from secret import lock_folder
from verify import restore_folder
from database import init_db

def main():
    """Command-line entry point.

    Parses CLI arguments and dispatches commands:
    - "init-db": create the SQLite database and required table
    - "lock": prompt for a folder path and lock it (restrict access)
    - "restore": prompt for a folder path and restore access

    If no command is provided the database is initialized by default.
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser("init-db")
    subparsers.add_parser("lock")
    subparsers.add_parser("restore")

    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
    elif args.command == "lock":
        lock_folder()
    elif args.command == "restore":
        restore_folder()
    else:
        init_db()

if __name__ == "__main__":
    main()