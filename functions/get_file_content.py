import os
from config import MAX_CHARS
from functions.get_valid_path import get_valid_path


def get_file_content(working_directory, file_path):
    full_path = get_valid_path(working_directory, file_path, "read")

    if full_path.startswith("Error:"):
        return full_path
    
    is_file = os.path.isfile(full_path)

    if not is_file:
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) >= MAX_CHARS:
                return f"{file_content_string} [...File {file_path} truncated at 10000 characters]"
            
            return file_content_string
    except Exception as e:
        return f"Error: unable to read contents of file {file_path}"