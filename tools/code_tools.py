from typing_extensions import Annotated
import subprocess
import utils.constants

CODE_WORKING_FOLDER = utils.constants.LLM_WORKING_FOLDER + "/code"


def exec_shell_command(
    shell_command: Annotated[
        str,
        "The shell command to execute locally",
    ]
) -> Annotated[str, "The output of the command after execution"]:

    shell_command = f"cd {CODE_WORKING_FOLDER} && {shell_command}"
    return subprocess.check_output(
        f"{shell_command}",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )
