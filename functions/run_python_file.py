import os
import subprocess
import sys
from functions.get_valid_path import get_valid_path
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = get_valid_path(working_directory, file_path, "execute")

    if full_path.startswith("Error:"):
        return full_path
    
    if not os.path.exists(full_path):
        return f"Error: File \"{file_path}\" not found."
    
    if not full_path.endswith('.py'):
        return f"Error: \"{file_path}\" is not a Python file."
    
    print(full_path)
    
    try:
        cmd = [sys.executable, full_path, *args]
        response = subprocess.run(cmd, timeout=30, cwd=working_directory, capture_output=True, text=True)

        output = []
        if response.stdout:
            output.append(f"STDOUT:\n{response.stdout}")
        if response.stderr:
            output.append(f"STDERR:\n{response.stderr}")

        if response.returncode != 0:
            output.append(f"Process exited with code {response.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Runs a python file along with arguments if necessary",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file you want to run, relative to the working directory. If not provided the function will error.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to be passed to run the file",
            ),
        },
    ),
)