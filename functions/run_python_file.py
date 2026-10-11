import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, file_path))
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_path]
        if args:
            command.extend(args)

        obj = subprocess.run(command, capture_output=True, text=True, timeout=30)
        ans = ""
        if obj.returncode != 0:
            ans += "Process exited with code X\n"
        if not obj.stdout and not obj.stderr:
            ans += "No output produced\n" 
        elif obj.stdout:
            ans += f"STDOUT: {obj.stdout}"
        elif obj.stderr:
            ans += f"STDERR: {obj.stderr}"
        return ans
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified .py file relative to the working directory, optionally uses command line inputs, providing output message",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path":{
                    "type": "string",
                    "description": "File path to read the data from, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "List of additional strings that are to be used when executing the specified file",
                    "parameters": {
                        "items": "string",
                        "description": "Additional arguments that are to be passed to the function being executed"
                    }
                },
            },
            "required": ["file_path"],
        },
    },
}