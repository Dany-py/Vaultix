import argparse
import sys
from cli import cli
from gui import gui
from database import init_db

def main():
    parser = argparse.ArgumentParser(description='Vaultix - Folder locking utility')
    subparsers = parser.add_subparsers(dest="command", help='Available commands')
    
    subparsers.add_parser("init-db", help="Initialize the database")
    subparsers.add_parser("lock", help="Lock a folder")
    subparsers.add_parser("restore", help="Restore a locked folder")
    
    parser.add_argument('--gui', action='store_true', default=False, help='Force GUI mode (default)')
    
    args = parser.parse_args()

    if args.command:
        init_db()
        cli()
    else:
        init_db()
        gui()

if __name__ == "__main__":
    main()