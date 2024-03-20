from langchain.tools import tool


class FileTools:

    @tool("Write File with content")
    def write_file(file_name, data):
        """Useful to write a file to a given path with a given content.
        The input to this tool should the file_name (no directory) as first argument,
        and file_content as second argument.
        """
        try:
            path = f"./llm_working_folder/{file_name}"
            with open(path, "w") as f:
                f.write(data)
            return f"File written to {path}."
        except Exception:
            return "Error with the input format for the tool."
