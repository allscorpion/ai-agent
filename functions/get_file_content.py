import os
from config import MAX_CHARS
from functions.get_valid_path import get_valid_path
from google.genai import types

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
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Get the contents of a file as a string, limited to {MAX_CHARS}",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path you want to read, relative to the working directory. If not provided the function will error.",
            ),
        },
    ),
)