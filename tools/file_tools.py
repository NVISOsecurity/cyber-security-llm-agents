from PyPDF2 import PdfReader
from langchain.tools import tool
from utilities import config_utils
import re


class FileTools:
    @tool("Write string to a file")
    def write_file(file_name, data):
        """Useful to write a file to a given path with a given content.
        The input to this tool should the file_name (no directory) as first argument as a string,
        and file_content as a string as second argument.
        """
        try:
            path = f"./{config_utils.LLM_WORKING_FOLDER}/{file_name}"
            with open(path, "w") as f:
                f.write(data)
            return f"File written to {path}."
        except Exception:
            return "Error with the input format for the tool."

    @tool("Read the content of a PDF document")
    def read_pdf_content(file_path):
        """
        Fetches and preprocesses content from a PDF given its file name in the local folder.
        Returns the text of the PDF.
        """
        path = f"./{file_path}"
        try:
            with open(path, "rb") as f:
                pdf = PdfReader(f)
                text = "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )

            # Optional preprocessing of text
            processed_text = re.sub(r"\s+", " ", text).strip()
            return processed_text
        except Exception as e:
            return f"Error reading the PDF file: {e}"
