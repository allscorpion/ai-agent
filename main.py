import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
import sys 
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if (len(sys.argv) <= 1):
    print("make sure to provide a prompt")
    sys.exit(1)

def call_function(function_call_part, verbose=False):
    if (verbose):
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    result = None
    match (function_call_part.name):
        case "get_file_content":
            result = get_file_content("./calculator", **function_call_part.args)
        case "get_files_info":
            result = get_files_info("./calculator", **function_call_part.args)
        case "run_python_file":
            result = run_python_file("./calculator", **function_call_part.args)
        case "write_file":
            result = write_file("./calculator", **function_call_part.args)

    if result == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )
            


def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    user_prompt = sys.argv[1]
    is_verbose = "--verbose" in sys.argv

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
    )

    if (is_verbose):
        print(f"User prompt: {user_prompt}")
        if (response.usage_metadata):
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            func_response = call_function(function_call_part, verbose=is_verbose)
            if func_response.parts and func_response.parts[0].function_response:
                response = func_response.parts[0].function_response.response

                if not response:
                    raise Exception("no function response returned")
                elif is_verbose:
                    print(f"-> {response}")

            else:
                raise Exception("no function response returned")
    else:
        print(response.text)
        

if __name__ == "__main__":
    main()