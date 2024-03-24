from langchain.tools import tool
from utilities import logging_utils, crew_utils
from time import sleep

import subprocess
import json
import base64


class APITools:
    @tool("Request documentation on the available data models for the Caldera API.")
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

    @tool("Request documentation on the available endpoints for the Caldera API.")
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

        ## Try to load the output as JSON
        # parsed_json = json.loads(command_output)
        ## If the above succeeds, pretty print the JSON output
        # return json.dumps(parsed_json, indent=4, sort_keys=True)

    @tool("Send request to the Caldera API")
    def caldera_api_request(command):
        """Expects a single parameter called "command" that represents a curl command that will be executed on the command line.
        You should always use "jq ." as filter to correctly format JSON.
        You are allowed to modify the jq filter to include or exclude certain fields in the results.
        You should reach the Caldera API at http://ubuntu-vm:8888/api/ and use the KEY:ADMIN123 header.
        Example: curl -H \"KEY:ADMIN123\" -sS http://ubuntu-vm:8888/api/abilities | jq . | grep "name"
        """
        try:
            command_output = subprocess.check_output(
                str(command), shell=True, stderr=subprocess.STDOUT, text=True
            )
            print(command_output)

            # Try to load the output as JSON
            parsed_json = json.loads(command_output)
            # If the above succeeds, pretty print the JSON output
            return_value = json.dumps(parsed_json, indent=4, sort_keys=True)

        except json.JSONDecodeError:
            # If the output is not valid JSON, return the original output
            return_value = command_output
        except subprocess.CalledProcessError as e:
            # Handle potential errors from the subprocess call
            logging_utils.logger.error(f"An error occurred: {e.output}")
            return_value = e.output

        return crew_utils.truncate_output(return_value)

    @tool("Change the command of the ability using the Caldera API")
    def caldera_update_ability_api_request(paw, command):
        """
        Expects two parameters: "paw" being the Caldera paw ID of the agent, "command" being the Windows command to execute.
        """
        command_template = """
            curl -s 'http://ubuntu-vm:8888/api/v2/operations/4daa339f-b50e-494d-bc8d-57829929764c/potential-links' \
            -H 'KEY: ADMIN123' \
            -H 'Content-Type: application/json' \
            --data-raw '{}'
            """

        # The arguments to be included in the command
        command_arguments = {
            "paw": paw,
            "executor": {
                "name": "psh",
                "platform": "windows",
                "command": command,
                "code": None,
                "language": None,
                "build_target": None,
                "payloads": [],
                "uploads": [],
                "timeout": 60,
                "parsers": [],
                "cleanup": [],
                "variations": [],
                "additional_info": {},
            },
        }

        # Convert the arguments to a JSON string
        json_data = json.dumps(command_arguments)

        # Insert the JSON string into the command
        final_command = command_template.format(json_data)

        try:

            command_output = subprocess.check_output(
                str(final_command), shell=True, stderr=subprocess.STDOUT, text=True
            )

            # Try to load the output as JSON
            parsed_json = json.loads(command_output)

            # Now we need to request the results of the operation
            # Do this by extracting the link ID from the response
            link_id = parsed_json["id"]

            # Now we can request the results of the operation
            final_command = f"""
                curl -s 'http://ubuntu-vm:8888/api/v2/operations/4daa339f-b50e-494d-bc8d-57829929764c/links/{link_id}/result' \
                -H 'KEY: ADMIN123'
                """

            # Parse output
            sleep(2)
            command_output = subprocess.check_output(
                str(final_command), shell=True, stderr=subprocess.STDOUT, text=True
            )
            # print(json.loads(command_output))
            # If the above succeeds, pretty print the JSON output
            return_value = "Command result: " + base64.b64decode(
                json.loads(command_output)["result"]
            ).decode("utf-8")

        except json.JSONDecodeError:
            # If the output is not valid JSON, return the original output
            return_value = command_output
        except subprocess.CalledProcessError as e:
            # Handle potential errors from the subprocess call
            logging_utils.logger.error(f"An error occurred: {e.output}")
            return_value = e.output

        return crew_utils.truncate_output(return_value)
