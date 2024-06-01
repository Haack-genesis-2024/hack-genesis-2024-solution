from os import path, makedirs, listdir, remove
from werkzeug.datastructures import FileStorage
import shutil

script_dir = path.dirname(path.abspath(__file__))

def get_user_files_folder(user_id: str):
    return path.join(script_dir, 'files', user_id);

def read_secret_key():
    filepath = path.join(script_dir, 'session-key.secret')
    try:
        with open(filepath, 'r') as secret_key_file:
            secret_key = secret_key_file.read().strip()
        return secret_key
    except FileNotFoundError:
        print(f"session-key.secret not found. Please ensure the file exists.")
        exit()

def save_user_file(user_id: str, file: FileStorage):
    directory = get_user_files_folder(user_id)

    if not path.exists(directory):
        makedirs(directory)
    
    file.save(path.join(directory, file.filename))


def delete_user_files(user_id: str):
    directory = get_user_files_folder(user_id)

    if path.exists(directory):
        shutil.rmtree(directory)

def get_user_files(user_id: str):
    directory = get_user_files_folder(user_id)

    if path.exists(directory):
        return listdir(directory)
    
    return []

def delete_user_file(user_id: str, file_name: str):
    directory = get_user_files_folder(user_id)
    file_path = path.join(directory, file_name)

    if path.exists(file_path):
        remove(file_path)
    else:
        raise FileNotFoundError(f"The file {file_name} does not exist.")
