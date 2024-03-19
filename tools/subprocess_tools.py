from langchain_core.tools import BaseTool
import subprocess


class SubprocessTool(BaseTool):
    name: str = "Subprocess execution tool"
    description: str = (
        "Execute a command as a subprocess and return the result. Use curl if the command is related to an API request. The argument should be a single string, e.g. 'curl https://api.example.com' or 'ls -l'."
    )

    def _run(self, argument: str) -> str:
        command_output = subprocess.check_output(
            argument, shell=True, stderr=subprocess.STDOUT, text=True
        )

        return command_output
