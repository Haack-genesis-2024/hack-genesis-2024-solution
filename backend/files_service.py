from os import path, makedirs, listdir, remove
from werkzeug.datastructures import FileStorage
import save_pdf

script_dir = path.dirname(path.abspath(__file__))
files_folder = path.join(script_dir, 'files')

def get_files_folder():
    if not path.exists(files_folder):
        makedirs(files_folder)
    return files_folder

def save_file(file: FileStorage):
    file_folder = get_files_folder()
    file.save(path.join(file_folder, file.filename))
    save_pdf.process_pdf_array([path.join(file_folder, file.filename)], 'opensearch-node1')

def get_files():
    file_folder = get_files_folder()
    return listdir(file_folder)

def delete_file(file_name: str):
    file_folder = get_files_folder()
    file_path = path.join(file_folder, file_name)

    if path.exists(file_path):
        remove(file_path)
    else:
        raise FileNotFoundError(f"The file {file_name} does not exist.")
