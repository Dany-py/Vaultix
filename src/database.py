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
                            folder TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            is_locked INTEGER DEFAULT 1,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                        );
        """)
        cursor.execute("""
                        CREATE TRIGGER IF NOT EXISTS update_folders_time 
                        AFTER UPDATE ON folders
                        BEGIN
                            UPDATE folders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                        END;
                    """
        )
        connection.commit()
        print(colored('Database initialized successfully !', "green"))

def load_data():
    try:
        with sqlite3.connect("folder.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT folder, is_locked, created_at, updated_at FROM folders")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Une erreur est survenue lors de la lecture de la base de données : {e}")
        return None

if __name__ == "__main__":
    init_db()