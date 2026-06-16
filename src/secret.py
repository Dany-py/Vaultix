import os
import bcrypt
import getpass
import sqlite3
import platform
import subprocess
from termcolor import colored

user = os.getlogin()


def confirm_pass(password: str, confirm: str) -> bool:
    """Return True if `password` and `confirm` are identical.

    This helper centralizes the equality check so callers can reuse it
    and makes unit testing straightforward.
    """
    return password == confirm


def lock_folder(**kwargs) -> tuple[bool, str]:
    """Lock a folder by storing a password hash and changing filesystem ACLs.

    Steps performed:
    - Ask the user for the folder path to protect.
    - Prompt for a password and confirmation until they match.
    - Hash the password with bcrypt and store the (path, hash) pair in
      the `folders` table inside `folder.db`.
    - On Windows, call `icacls` to remove inheritance and deny the
      current user full control over the folder, effectively hiding it.

    Note: This function currently uses Windows `icacls`. Running it on
    non-Windows platforms will likely fail. The stored hash allows
    restoring access later via `restore_folder`.
    """
    try:
        secret_path = kwargs.get('path') if kwargs else input('Paste or write the path you want to keep secret: ')
        
        # Nettoyer et normaliser le chemin
        secret_path = secret_path.strip()
        secret_path = os.path.normpath(secret_path)
        #secret_path = os.path.abspath(secret_path)
        
        if not os.path.exists(secret_path):
            if kwargs:
                print('Path :', secret_path)
                return False, f"Path does not exist: {secret_path}"
            else:
                raise(colored("Path does not exist.", "red"))
        
        while True:
            password = kwargs.get('pwd') if kwargs else getpass.getpass("Enter your secret password: ")
            confirm = kwargs.get('cf_pwd') if kwargs else getpass.getpass("Confirm password: ")
            if confirm_pass(password, confirm):
                break
            print(colored("Passwords don't match. Please try again.\n", "red"))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        with sqlite3.connect("folder.db") as connection:    
            cursor = connection.cursor()
            folder_data = (secret_path, hashed_password)
            cursor.execute("INSERT INTO folders (folder, password) VALUES (?, ?)", folder_data)
            connection.commit()

        result = subprocess.run(f'icacls "{secret_path}" /inheritance:r /deny "{user}:(OI)(CI)(F)"',shell=True)
        if result.returncode != 0:
            return False, "Failed to restrict access !"
        else:
            return True, "Folder access restricted !"
    except ValueError as e:
        return False, str(e)
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    except OSError as e:
        return False, f"System error: {e}"

if __name__ == "__main__":
    lock_folder()