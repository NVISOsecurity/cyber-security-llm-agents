from langchain.tools import tool
from utilities import logging_utils, crew_utils

import subprocess
import json


class APITools:

    @tool("Send request to API")
    def api_request(curl_command):
        """Useful to send a request to an API using curl.
        Important is to run curl with -sS arguments.
        The input to this tool should be a single curl command we can run on the command line.
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
