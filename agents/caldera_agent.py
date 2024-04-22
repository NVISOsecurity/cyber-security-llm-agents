from os import system
from autogen import AssistantAgent
from utils.shared_config import config_list
from autogen import ConversableAgent
import utils.constants
from tools.web_tools import download_web_page

from tools.caldera_tools import (
    caldera_api_request,
    caldera_api_method_details,
    caldera_swagger_info,
    caldera_api_get_operation_info,
    caldera_execute_command_on_agent,
    caldera_upload_file_from_agent,
)

caldera_agent = ConversableAgent(
    "caldera_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    description="A helpful agent that can help decide which Caldera actions to take next.",
)

caldera_agent_user_proxy = ConversableAgent(
    "caldera_agent_user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
)

### Swagger info

caldera_agent.register_for_llm(
    name="caldera_swagger_info",
    description="Retrieve the list of all available Caldera API methods along with a description of their functionality",
)(caldera_swagger_info)

caldera_agent_user_proxy.register_for_execution(name="caldera_swagger_info")(
    caldera_swagger_info
)

# Get details on a specific API method

caldera_agent.register_for_llm(
    name="caldera_api_method_details",
    description="Retrieve the details on a specific API method in Caldera including the parameters it takes and the responses it returns.",
)(caldera_api_method_details)

caldera_agent_user_proxy.register_for_execution(name="caldera_api_method_details")(
    caldera_api_method_details
)

# Perform an API request to Caldera

caldera_agent.register_for_llm(
    name="caldera_api_request",
    description="Perform an API request to Caldera based on the given API method extracted from the Swagger documentation.",
)(caldera_api_request)

caldera_agent_user_proxy.register_for_execution(name="caldera_api_request")(
    caldera_api_request
)

# Get the ID of the active Caldera Operation

caldera_agent.register_for_llm(
    name="caldera_api_get_operation_info",
    description="Get the ID of the active Caldera Operation",
)(caldera_api_get_operation_info)

caldera_agent_user_proxy.register_for_execution(name="caldera_api_get_operation_info")(
    caldera_api_get_operation_info
)

# Exfiltrate file over FTP

caldera_agent.register_for_llm(
    name="caldera_upload_file_from_agent",
    description="Upload a file from the agent to the Caldera server using FTP.",
)(caldera_upload_file_from_agent)

caldera_agent_user_proxy.register_for_execution(name="caldera_upload_file_from_agent")(
    caldera_upload_file_from_agent
)

# Execute a command on a specific agent

caldera_agent.register_for_llm(
    name="caldera_execute_command_on_agent",
    description="Execute a command on a specific agent",
)(caldera_execute_command_on_agent)

caldera_agent_user_proxy.register_for_execution(
    name="caldera_execute_command_on_agent"
)(caldera_execute_command_on_agent)

# Download a web page

caldera_agent.register_for_llm(
    name="download_web_page",
    description="Download the content of a web page and return it as a string. Only for text content such as markdown pages.",
)(download_web_page)

caldera_agent_user_proxy.register_for_execution(name="download_web_page")(
    download_web_page
)
