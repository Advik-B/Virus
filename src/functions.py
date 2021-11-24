#!bin/env python3

import os
import fnmatch
import shutil

from cryptography.fernet import Fernet

def list_files(cwd: str, pattern: str, match_without_extension: bool=False) -> list:
    """
    Returns a list of all files in a directory and its subdirectories that match a given pattern.
    """

    filenames_ = []
    for dirpath, _, filenames in os.walk(cwd):
        for f in filenames:
            if fnmatch.fnmatch(f, pattern):
                filenames_.append(os.path.join(dirpath, f))
            else:
                f_list = f.split('.')
                if len(f_list) == 1 and match_without_extension and not f.endswith('.key'):
                    filenames_.append(os.path.join(dirpath, f))
    del _, filenames, dirpath # Clean up unused variables to free memory.
    return filenames_

def encrypt_files(filenames: list, key: str) -> None:
    """
    Encrypts a list of files using a given key.
    """
    frenet = Fernet(key)
    for f in filenames:
        with open(f, 'rb') as f_in:
            original_data = f_in.read()
            
        with open(f, 'wb') as f_out:
            encrypted_data = frenet.encrypt(original_data)
            f_out.write(encrypted_data)
        
def decrypt_files(filenames: list, key: str) -> None:
    """
    Decrypts a list of files using a given key.
    """
    fernet = Fernet(key)
    for f in filenames:
        with open(f, 'rb') as f_in:
            encrypted_data = f_in.read()
        with open(f, 'wb') as f_out:
            original_data = fernet.decrypt(encrypted_data)
            f_out.write(original_data)

def get_key() -> str:
    """
    Generates a random key.
    """
    key_path = os.path.join(os.path.expanduser('~'), 'key.key')
    key = Fernet.generate_key()
    
    if os.path.isfile(key_path):
        with open(key_path, 'rb') as f:
            key = f.read()
    elif os.path.isdir(key_path):
        shutil.rmtree(key_path, ignore_errors=True)
    else:
        with open(key_path, 'wb') as f:
            f.write(key)

    return key

# End of file.