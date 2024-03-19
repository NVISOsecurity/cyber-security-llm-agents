from langchain.tools import tool


class FileTools:

    @tool("Write File with content")
    def write_file(data: str):
        """Useful to write a file to a given path with a given content.
        The input to this tool should be a pipe (|) separated text
        of length two, representing the name of the file excluding the direcory,
        and the content you want to write to it.
        For example, `report.txt|FILE_PLACEHOLDER`.
        Replace FILE_PLACEHOLDER with the actual data you want to write to the file."""
        try:
            path, content = data.split("|")
            path = f"./llm_working_folder/{path}"
            with open(path, "w") as f:
                f.write(content)
            return f"File written to {path}."
        except Exception:
            return "Error with the input format for the tool."
