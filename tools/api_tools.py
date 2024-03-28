from langchain.tools import tool
from utilities import crew_utils
from time import sleep

import subprocess
import json
import base64


def caldera_api_get_agents():
    """Does not take any arguments.
    Returns the list of available agents by querying the Caldera API.
    """
    command_output = subprocess.check_output(
        str(
            "curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/agents | jq '.[0].paw'"
        ),
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return command_output.replace('"', "")


def caldera_api_get_operation_info():
    """Requires no arguments.
    Returns information on the active operation by querying the Caldera API.
    """
    command_output = subprocess.check_output(
        str(
            "curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/operations | jq '.[0].id'"
        ),
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )

    return command_output.replace('"', "")


class APITools:
    @tool("Request documentation on the available data models for the Caldera API")
    def caldera_api_available_models(scope):
        """Requires a single argument 'scope' being either Agent, Adversary, Ability or Operation.
        The data returned is documentation which  should be used to then request the actual data from the API.
        """
        command_output = subprocess.check_output(
            str(
                "curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/docs/swagger.json | jq .definitions | jq 'to_entries | map(select(.key | startswith(\""
                + str(scope)
                + "\"))) | from_entries'"
            ),
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
        )

        return (
            command_output
            + " \n\n THE ABOVE IS DOCUMENTATION ONLY. NOW USE THE API TO REQUEST DATA BASED ON WHAT IS DESCRIBED IN THIS DOCUMENTATION."
        )
        ## Try to load the output as JSON
        # parsed_json = json.loads(command_output)
        ## If the above succeeds, pretty print the JSON output
        # return json.dumps(parsed_json, indent=4, sort_keys=True)

    @tool("Request documentation on the available endpoints for the Caldera API")
    def caldera_api_available_functions(scope):
        """Requires a single argument 'scope' being either agents, adversaries, abilities or operations.
        This tool will return the available functions for the specified scope.
        The data returned is documentation which  should be used to then request the actual data from the API.
        """
        command_output = subprocess.check_output(
            str(
                "curl -H 'KEY:ADMIN123' -sS http://ubuntu-vm:8888/api/docs/swagger.json | jq .paths | jq 'to_entries | map(select(.key | startswith(\"/api/v2/"
                + str(scope)
                + "\"))) | from_entries'"
            ),
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
        )

        return (
            command_output
            + " \n\n THE ABOVE IS DOCUMENTATION ONLY. NOW USE THE API TO REQUEST DATA BASED ON WHAT IS DESCRIBED IN THIS DOCUMENTATION."
        )

    @tool("Run a Powershell command on a Caldera agent and return the output.")
    def caldera_execute_command_on_agent(command):
        """Expects a single parameter: "command" being the Powershell command to execute."""

        agent_paw = caldera_api_get_agents().strip()
        operation_id = caldera_api_get_operation_info().strip()

        command_arguments = {
            "paw": agent_paw,
            "executor": {
                "name": "psh",
                "platform": "windows",
                "command": command,
            },
        }

        # Write the command to a file
        with open("./llm_working_folder/parameters.json", "w") as f:
            f.write(json.dumps(command_arguments))

        command_template = f"""
        curl -s 'http://ubuntu-vm:8888/api/v2/operations/{operation_id}/potential-links' \
        -H 'KEY: ADMIN123' \
        -H 'Content-Type: application/json' \
        --data-binary @llm_working_folder/parameters.json
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
                return_value = command_output

        except json.JSONDecodeError as e:
            # If the output is not valid JSON, return the original output
            return_value = e
        except subprocess.CalledProcessError as e:
            # Handle potential errors from the subprocess call
            return_value = str(e)

        return crew_utils.truncate_output(return_value)
