import subprocess
from typing_extensions import Annotated
import tiktoken
from autogen.agentchat.contrib.capabilities.context_handling import (
    truncate_str_to_tokens,
)


def caldera_api_method_details(
    api_method: Annotated[
        str,
        "The Caldera API for which you want the full details, starting with api/v2/",
    ]
) -> Annotated[str, "The details of the API method"]:

    return subprocess.check_output(
        f"curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/docs/swagger.json | jq '.paths[\"{api_method}\"]'",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )


def caldera_api_request(
    api_method: Annotated[
        str,
        "The Caldera API path to request, for example api/v2/agents",
    ],
    jq_filter: Annotated[
        str,
        "The optional jq filter to apply to the output of the API request, defaults to .",
    ] = ".",
) -> Annotated[
    str, "The output of the API request to the Caldera server for the given API method"
]:

    command_to_run = f"curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/{api_method} | jq '{jq_filter}'"
    try:
        output = subprocess.check_output(
            command_to_run,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
        )

    except subprocess.CalledProcessError as e:
        # This will be reached if the command returned a non-zero exit status
        error_output = e.output  # The error output is stored in the output attribute
        return_code = e.returncode  # You can also get the return code of the command
        # Handle the error output and return code as needed
        return_info = (
            f"The command '{command_to_run}' failed with exit code {return_code}."
        )
        return_info += "Error output:"
        return_info += error_output
    else:
        # This will be reached if the command was successful
        # The output variable contains the command's output
        return_info = "The command was successful with the following output:"
        return_info += output

    # Truncate the output to 1000 characters
    # Also print a message to indicate that the output was truncated including the number of characters
    # TODO: Investigate why MessageTokenLimiter is not working as expected for this!
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return truncate_str_to_tokens(return_info, 4000)


def caldera_swagger_info() -> Annotated[
    str,
    "The list of all available Caldera API methods along with a description of their functionality",
]:

    return subprocess.check_output(
        str(
            "curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/docs/swagger.json | jq '.paths | to_entries[] | {path: .key, description: .value | to_entries[] | .value.description}'"
        ),
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )
