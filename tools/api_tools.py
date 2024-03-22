from langchain.tools import tool
from utilities import logging_utils, crew_utils

import subprocess
import json


class APITools:
    @tool("Request the available models for the Caldera API")
    def caldera_api_available_models(scope):
        """Requires a single argument 'scope' being either Ability or Operation."""
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

        # Try to load the output as JSON
        parsed_json = json.loads(command_output)
        # If the above succeeds, pretty print the JSON output
        return json.dumps(parsed_json, indent=4, sort_keys=True)

    @tool("Request the available functions for the Caldera API")
    def caldera_api_available_functions(scope):
        """Requires a single argument 'scope' being either abilities or operations."""
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

        # Try to load the output as JSON
        parsed_json = json.loads(command_output)
        # If the above succeeds, pretty print the JSON output
        return json.dumps(parsed_json, indent=4, sort_keys=True)

    @tool("Send request to the Caldera API")
    def caldera_api_request(command):
        """Expects a single command line argument "command" that will be executed on the command line.
        You will need to issue HTTP requests to http://ubuntu-vm:8888/api/ to interact with the Caldera API.
        Always add the authorization header -H \"KEY:ADMIN123\" to curl commands.

        You can use the following endpoints:
            + /api/v2/abilities

        Important is to run curl with -sS arguments.
        ALWAYS add additional filters to avoid a large API response, and leave the 'jq .' part untouched to pretty print the JSON before applying other filters.
        Example: curl --H <headers> -sS <URL> | jq . | <additional filters using jq, grep, ...>
        """
        try:
            command_output = subprocess.check_output(
                str(command), shell=True, stderr=subprocess.STDOUT, text=True
            )

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
