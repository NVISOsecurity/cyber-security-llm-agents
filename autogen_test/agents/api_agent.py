from autogen import AssistantAgent
from utils.shared_config import config_list

from tools.caldera_tools import (
    caldera_api_request,
    caldera_api_method_details,
    caldera_swagger_info,
)


api_agent = AssistantAgent(
    "api_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
)

api_agent.register_for_llm(
    name="caldera_swagger_info",
    description="Retrieve the list of all available Caldera API methods along with a description of their functionality",
)(caldera_swagger_info)

api_agent.register_for_llm(
    name="caldera_api_method_details",
    description="Retrieve the details on a specific API method in Caldera including the parameters it takes and the responses it returns.",
)(caldera_api_method_details)

api_agent.register_for_llm(
    name="caldera_api_request",
    description="Perform an API request to Caldera based on the given API method extracted from the Swagger documentation.",
)(caldera_api_request)
