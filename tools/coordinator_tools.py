from PyPDF2 import PdfReader
from langchain.tools import tool
from utilities import config_utils
import re


class CoordinatorTools:

    @tool("Write a detailed description of the task results to the progress file.")
    def add_task_results_to_progress_file(task_results):
        """Takes a single argument 'task_results' which is a string.
        The input to this tool should be a string with the following format.

        Example:
        The list of agents was retrieved successfully (paw: <paw id>)
        The command <full commmand> was ran successfully and returned <output> (paw: <paw id>)
        I ran into an issue with the command <full command> and the error was <error message> (paw: <paw id>)
        """
        try:
            path = f"./{config_utils.LLM_WORKING_FOLDER}/progress.txt"
            # append
            with open(path, "a") as f:
                f.write(str(task_results))
                f.write("\n===================\n")
            return f"File written to {path}."
        except Exception:
            return "Error with the input format for the tool."

    @tool("Read the progress file to understand the current state of the workflow")
    def retrieve_progress_file():
        """
        Does not take any arguments.
        Returns the content of the progress file.
        """
        path = f"./{config_utils.LLM_WORKING_FOLDER}/progress.txt"

        try:
            # Create file if it does not exist
            with open(path, "a") as f:
                pass
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading the progress file: {e}"
