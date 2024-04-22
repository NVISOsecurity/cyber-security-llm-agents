from langchain_core.tools import BaseTool
from utilities import crew_utils

import subprocess


class SubprocessTool(BaseTool):
    name: str = "Subprocess execution tool"
    description: str = (
        "Execute a command as a subprocess and return the result. You can pipe different commands."
    )

    def _run(self, argument: str) -> str:
        command_output = subprocess.check_output(
            argument, shell=True, stderr=subprocess.STDOUT, text=True
        )

        return crew_utils.truncate_output_end(command_output)
