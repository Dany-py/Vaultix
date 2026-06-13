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


def lock_folder():
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

    secret_path = input('Paste or write the path you want to keep secret: ')

    while True:
        password = getpass.getpass("Enter your secret password: ")
        confirm = getpass.getpass("Confirm password: ")
        if confirm_pass(password, confirm):
            break
        print(colored("Passwords don't match. Please try again.\n", "red"))

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with sqlite3.connect("folder.db") as connection:    
        cursor = connection.cursor()
        folder_data = (secret_path, hashed_password)
        cursor.execute("INSERT INTO folders (folder, password) VALUES (?, ?)", folder_data)
        connection.commit()

    subprocess.run(f'icacls "{secret_path}" /inheritance:r /deny "{user}:(OI)(CI)(F)"',shell=True)
    print(colored("Folder access restricted !", "yellow"))

if __name__ == "__main__":
    lock_folder()