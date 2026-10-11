import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_path, directory))
        common_path = os.path.commonpath([absolute_path, full_path])
        check_valid = common_path == absolute_path
        if not check_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        ans = []
        for entry in os.scandir(full_path):
            file_name = entry.name   
            file_size = os.path.getsize(entry.path)
            is_dir = entry.is_dir()
            to_push = f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            ans.append(to_push)
        ans = "\n".join(ans)
        return ans
    except Exception as e:
        return f"Error: {e}"
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}