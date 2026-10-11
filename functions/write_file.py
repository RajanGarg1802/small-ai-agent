import os
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, file_path))
        common_path = os.path.commonpath([absolute_path, full_path])
        if common_path != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrites a file at the specified file path in the working directory, writing the specified content in the file",
        "parameters": {
            "type": "object",
            "properties":{
                "file_path": {
                    "type": "string",
                    "description": "File Path to write at, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The data to write to the specified file"
                },
            },
            "required": ["file_path", "content"],
        },
    },
}