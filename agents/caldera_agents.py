from utils.shared_config import llm_config

from autogen import ConversableAgent
from agents.text_agents import (
    task_coordinator_agent,
)

from tools.caldera_tools import (
    caldera_api_request,
    caldera_api_method_details,
    caldera_swagger_info,
    caldera_api_get_operation_info,
    caldera_execute_command_on_agent,
    caldera_upload_file_from_agent,
    caldera_service_list,
    caldera_create_adversary_profile,
    caldera_add_abilities_to_adversary_profile,
    match_techniques_to_caldera_abilities,
)

caldera_agent = ConversableAgent(
    name="caldera_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant that can interact with Caldera agents""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)


def register_tools():
    # Service List
    caldera_agent.register_for_llm(
        name="caldera_service_list",
        description="Retrieve the list of all running services on the Caldera agent.",
    )(caldera_service_list)

    task_coordinator_agent.register_for_execution(name="caldera_service_list")(
        caldera_service_list
    )

    # Swagger info

    caldera_agent.register_for_llm(
        name="caldera_swagger_info",
        description="Retrieve the list of all available Caldera API methods along with a description of their functionality",
    )(caldera_swagger_info)

    task_coordinator_agent.register_for_execution(name="caldera_swagger_info")(
        caldera_swagger_info
    )

    # Get details on a specific API method

    caldera_agent.register_for_llm(
        name="caldera_api_method_details",
        description="Retrieve the details on a specific API method in Caldera including the parameters it takes and the responses it returns.",
    )(caldera_api_method_details)

    task_coordinator_agent.register_for_execution(name="caldera_api_method_details")(
        caldera_api_method_details
    )

    # Perform an API request to Caldera

    caldera_agent.register_for_llm(
        name="caldera_api_request",
        description="Perform an API request to Caldera based on the given API method extracted from the Swagger documentation.",
    )(caldera_api_request)

    task_coordinator_agent.register_for_execution(name="caldera_api_request")(
        caldera_api_request
    )

    # Create an Adversary profile in Caldera

    caldera_agent.register_for_llm(
        name="caldera_create_adversary_profile",
        description="Create an Adversary profile in Caldera",
    )(caldera_create_adversary_profile)

    task_coordinator_agent.register_for_execution(name="caldera_create_adversary_profile")(
        caldera_create_adversary_profile
    )

    # Add abilities to an Adversary profile in Caldera

    caldera_agent.register_for_llm(
        name="caldera_add_abilities_to_adversary_profile",
        description="Add abilities to an Adversary profile in Caldera",
    )(caldera_add_abilities_to_adversary_profile)

    task_coordinator_agent.register_for_execution(name="caldera_add_abilities_to_adversary_profile")(
        caldera_add_abilities_to_adversary_profile
    )

    # Get the ID of the active Caldera Operation

    caldera_agent.register_for_llm(
        name="caldera_api_get_operation_info",
        description="Get the ID of the active Caldera Operation",
    )(caldera_api_get_operation_info)

    task_coordinator_agent.register_for_execution(
        name="caldera_api_get_operation_info"
    )(caldera_api_get_operation_info)

    # Exfiltrate file over FTP

    caldera_agent.register_for_llm(
        name="caldera_upload_file_from_agent",
        description="Upload a file from the agent to the Caldera server using FTP.",
    )(caldera_upload_file_from_agent)

    task_coordinator_agent.register_for_execution(
        name="caldera_upload_file_from_agent"
    )(caldera_upload_file_from_agent)

    # Execute a command on a specific agent

    caldera_agent.register_for_llm(
        name="caldera_execute_command_on_agent",
        description="Execute a command on a specific agent",
    )(caldera_execute_command_on_agent)

    task_coordinator_agent.register_for_execution(
        name="caldera_execute_command_on_agent"
    )(caldera_execute_command_on_agent)


    # Match techniques to Caldera abilities

    caldera_agent.register_for_llm(
        name="match_techniques_to_caldera_abilities",
        description="Match techniques to Caldera abilities",
    )(match_techniques_to_caldera_abilities)

    task_coordinator_agent.register_for_execution(name="match_techniques_to_caldera_abilities")(
        match_techniques_to_caldera_abilities
    )
