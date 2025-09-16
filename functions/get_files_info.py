import os

from functions.get_valid_path import get_valid_path

def get_files_info(working_directory, directory="."):
    full_path = get_valid_path(working_directory, directory, "read")

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


    

