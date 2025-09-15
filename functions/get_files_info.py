import os

from config import MAX_CHARS


def get_valid_path(working_directory, path):
    full_path = os.path.join(working_directory, path)

    abs_path_work_dir = os.path.abspath(working_directory)
    abs_path_dir = os.path.abspath(full_path)

    if (not abs_path_dir.startswith(abs_path_work_dir)):
        return f'Error: Cannot read "{path}" as it is outside the permitted working directory'
    
    return abs_path_dir

def get_files_info(working_directory, directory="."):
    full_path = get_valid_path(working_directory, directory)

    if full_path.startswith("Error:"):
        return full_path
    
    is_directory = os.path.isdir(full_path)
    
    if not is_directory:
        return f'Error: "{directory}" is not a directory'
    
    output = []

    try:
        for item in os.listdir(full_path):
            full_item_path = os.path.join(full_path, item)
            output.append(f"- {item}: file_size={os.path.getsize(full_item_path)} bytes, is_dir={os.path.isfile(full_item_path)}")

        return "\n".join(output)
    except Exception as e:
        return f"Error listing files: {e}"

def get_file_content(working_directory, file_path):
    full_path = get_valid_path(working_directory, file_path)

    if full_path.startswith("Error:"):
        return full_path
    
    is_file = os.path.isfile(full_path)

    if not is_file:
        return f"Error: File not found or is not a regular file: {file_path}"
    
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) >= MAX_CHARS:
                return f"{file_content_string} [...File {file_path} truncated at 10000 characters]"
            
            return file_content_string
    except Exception as e:
        return f"Error: unable to read contents of file {file_path}"