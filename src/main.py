from functions import *
import os

cwd = os.getcwd()

key = get_key()

files = list_files(cwd, '*.*', True)

encrypt_files(files, key)

decrypt_files(files, key)
