import os
from functions.config import MAX_CHARS
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, file_path))
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        read_data = ""
        with open(full_path) as f:
            read_data = f.read(MAX_CHARS)
            if f.read(1):
                read_data += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return read_data
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a specified file path relative to the working directory, providing the data inside the file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read the data from, relative to the working directory"
                },
            },
        },
        "required": ["file_path"],
    },
}