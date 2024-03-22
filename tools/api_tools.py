from langchain.tools import tool
from utilities import logging_utils, crew_utils

import subprocess
import json


class APITools:

    @tool("Send request to the Caldera API")
    def caldera_api_request(curl_command):
        """Expects a single command line argument that will be executed on the command line.
        You will need to issue HTTP requests to http://ubuntu-vm:8888/api/ to interact with the Caldera API.
        Always add the authorization header -H \"KEY:BLUEADMIN123\" to curl commands.

        You can use the following endpoints:
            + /api/v2/abilities

        Important is to run curl with -sS arguments .
        ALWAYS use the following format, where you only use grep to filter out, and leave jq untouched to pretty print the JSON.
        Example: curl --H <headers> -sS <URL> | jq . | grep <filter>
        """
        try:
            command_output = subprocess.check_output(
                str(curl_command), shell=True, stderr=subprocess.STDOUT, text=True
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
