import json
from cryptography.fernet import Fernet
import os

PASSWORDS_FILE = 'passwords.json'
ENCRYPTION_KEY_FILE = 'key.key'

def password_manager(action, password=None, account=None):
    """Manages passwords with encryption."""
    key = load_encryption_key()
    passwords = load_passwords()

    if action == 'set' and password and account:
        encrypted_password = Fernet(key).encrypt(password.encode()).decode()
        passwords[account] = encrypted_password
        save_passwords(passwords)
        return f"Password for '{account}' has been set."
    
    elif action == 'retrieve' and account:
        if account in passwords:
            decrypted_password = Fernet(key).decrypt(passwords[account].encode()).decode()
            return f"The password for '{account}' is: {decrypted_password}"
        return "Account not found."
    
    return "Invalid action."

def load_encryption_key():
    """Loads or generates an encryption key."""
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return key

def load_passwords():
    """Loads passwords from the password file."""
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_passwords(passwords):
    """Saves passwords back to the file."""
    with open(PASSWORDS_FILE, 'w') as file:
        json.dump(passwords, file)
