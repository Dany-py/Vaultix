import sqlite3
from termcolor import colored


def init_db():
    """Initialize the SQLite database used by this project.

    Creates (if missing) a file-based SQLite database named `folder.db`
    and a single table `folders` to store folder paths and password hashes.
    Prints a success message on completion.
    """
    with sqlite3.connect("folder.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder TEXT NOT NULL,
                password TEXT
            )
        """)
        connection.commit()
        print(colored('Database initialized successfully !', "green"))

if __name__ == "__main__":
    init_db()