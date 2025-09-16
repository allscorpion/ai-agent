import os


def get_valid_path(working_directory, path, errorTag):
    full_path = os.path.join(working_directory, path)

    abs_path_work_dir = os.path.abspath(working_directory)
    abs_path_dir = os.path.abspath(full_path)

    if (not abs_path_dir.startswith(abs_path_work_dir)):
        return f'Error: Cannot {errorTag} "{path}" as it is outside the permitted working directory'
    
    return abs_path_dir