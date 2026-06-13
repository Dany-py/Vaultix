import os
import bcrypt
import getpass
import sqlite3
import platform
import subprocess
from termcolor import colored

user = os.getlogin()

def restore_folder():
    """Restore access to a previously locked folder.

    Workflow:
    - Prompt the user for the folder path they want to restore.
    - Look up the stored password hash in the `folders` table in `folder.db`.
    - Allow the user up to 3 attempts to enter the original password.
    - If the password matches, call Windows `icacls` to grant the current
      user full control of the folder again.

    Notes:
    - If the path is not found in the database the function exits with an
      error message and status code 1.
    - This function currently relies on Windows `icacls` and will fail on
      non-Windows platforms.
    """

    secret_path = input('Paste or write the path you want to restore: ')

    with sqlite3.connect("folder.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT folder, password FROM folders WHERE folder = ?", (secret_path,))
        folder = cursor.fetchone()

    if folder is None:
        print(colored("No records were found for this path.", "red"))
        raise SystemExit(1)

    stored_password_hash = folder[1]
    count = 3

    while count > 0 :
        password = getpass.getpass("Enter your secret password: ")
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            break
        print(colored("Passwords don't match. Please try again.\n", "red"))
        count -= 1
    
    if count == 0:
        print(colored("Too many failed attempts. Try again later.\n", "red"))
        return

    subprocess.run(f'icacls "{secret_path}" /grant "{user}:(OI)(CI)(F)"',shell=True)
    print(colored("Folder access restored !", "yellow"))


if __name__ == "__main__":
    restore_folder()