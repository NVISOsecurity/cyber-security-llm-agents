from langchain.tools import tool
from utilities import logging_utils, crew_utils

import subprocess
import json


class APITools:
    @tool("Request documentation on the available data models for the Caldera API.")
    def caldera_api_available_models(scope):
        """Requires a single argument 'scope' being either Agent, Ability or Operation.
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
        """Requires a single argument 'scope' being either agents, abilities or operations.
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
