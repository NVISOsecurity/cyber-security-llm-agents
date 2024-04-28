from autogen import ConversableAgent
from utils.shared_config import config_list
from tools.web_tools import download_web_page

from tools.caldera_tools import (
    caldera_api_request,
    caldera_api_method_details,
    caldera_swagger_info,
    caldera_api_get_operation_info,
    caldera_execute_command_on_agent,
    caldera_upload_file_from_agent,
    caldera_service_list,
)

task_coordinator_agent = ConversableAgent(
    name="task_coordinator_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant to solve tasks.""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)

security_analyst_agent = ConversableAgent(
    name="security_analyst_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant that can solve problems around cyber security.""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)

text_analyst_agent = ConversableAgent(
    name="text_analyst_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant to solve tasks.""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)


def register_tools():
    # Download a web page

    security_analyst_agent.register_for_llm(
        name="download_web_page",
        description="Download the content of a web page and return it as a string. Only for text content such as markdown pages.",
    )(download_web_page)

    task_coordinator_agent.register_for_execution(name="download_web_page")(
        download_web_page
    )

    ### Service List
    security_analyst_agent.register_for_llm(
        name="caldera_service_list",
        description="Retrieve the list of all running services on the Caldera agent.",
    )(caldera_service_list)

    task_coordinator_agent.register_for_execution(name="caldera_service_list")(
        caldera_service_list
    )

    ### Swagger info

    security_analyst_agent.register_for_llm(
        name="caldera_swagger_info",
        description="Retrieve the list of all available Caldera API methods along with a description of their functionality",
    )(caldera_swagger_info)

    task_coordinator_agent.register_for_execution(name="caldera_swagger_info")(
        caldera_swagger_info
    )

    # Get details on a specific API method

    security_analyst_agent.register_for_llm(
        name="caldera_api_method_details",
        description="Retrieve the details on a specific API method in Caldera including the parameters it takes and the responses it returns.",
    )(caldera_api_method_details)

    task_coordinator_agent.register_for_execution(name="caldera_api_method_details")(
        caldera_api_method_details
    )

    # Perform an API request to Caldera

    security_analyst_agent.register_for_llm(
        name="caldera_api_request",
        description="Perform an API request to Caldera based on the given API method extracted from the Swagger documentation.",
    )(caldera_api_request)

    task_coordinator_agent.register_for_execution(name="caldera_api_request")(
        caldera_api_request
    )

    # Get the ID of the active Caldera Operation

    security_analyst_agent.register_for_llm(
        name="caldera_api_get_operation_info",
        description="Get the ID of the active Caldera Operation",
    )(caldera_api_get_operation_info)

    task_coordinator_agent.register_for_execution(
        name="caldera_api_get_operation_info"
    )(caldera_api_get_operation_info)

    # Exfiltrate file over FTP

    security_analyst_agent.register_for_llm(
        name="caldera_upload_file_from_agent",
        description="Upload a file from the agent to the Caldera server using FTP.",
    )(caldera_upload_file_from_agent)

    task_coordinator_agent.register_for_execution(
        name="caldera_upload_file_from_agent"
    )(caldera_upload_file_from_agent)

    # Execute a command on a specific agent

    security_analyst_agent.register_for_llm(
        name="caldera_execute_command_on_agent",
        description="Execute a command on a specific agent",
    )(caldera_execute_command_on_agent)

    task_coordinator_agent.register_for_execution(
        name="caldera_execute_command_on_agent"
    )(caldera_execute_command_on_agent)

    # Download a web page

    security_analyst_agent.register_for_llm(
        name="download_web_page",
        description="Download the content of a web page and return it as a string. Only for text content such as markdown pages.",
    )(download_web_page)

    task_coordinator_agent.register_for_execution(name="download_web_page")(
        download_web_page
    )
