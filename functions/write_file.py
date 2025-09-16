import os
from functions.get_valid_path import get_valid_path
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = get_valid_path(working_directory, file_path, "write")

    if full_path.startswith("Error:"):
        return full_path
    
    try:
        dir_path = os.path.dirname(full_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception as e:
        return f"Error: unable to create directory for {file_path} {e}"

    try:    
        if os.path.exists(full_path) and os.path.isdir(full_path):
            return f'Error: "{file_path}" is a directory, not a file'
        
        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: unable to overwrite contents for {file_path} {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Write or overwrite the contents to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file you want to write the contents to, relative to the working directory. If not provided the function will error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents that you want to put into the file",
            ),
        },
    ),
)