from autogen import AssistantAgent
from utils.shared_config import config_list
from autogen import UserProxyAgent
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

caldera_agent = AssistantAgent(
    "caldera_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"].upper(),
)

caldera_agent_user_proxy = UserProxyAgent(
    "caldera_agent_user_proxy",
    code_execution_config={
        "work_dir": utils.constants.LLM_WORKING_FOLDER + "/caldera",
        "use_docker": False,
    },
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
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

# Exfiltrate file
caldera_agent.register_for_llm(
    name="caldera_upload_file_from_agent",
    description="Upload a file from the agent",
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

# Download documentation

caldera_agent.register_for_llm(
    name="download_web_page",
    description="Download the content of a web page and return it as a string.",
)(download_web_page)

caldera_agent_user_proxy.register_for_execution(name="download_web_page")(
    download_web_page
)