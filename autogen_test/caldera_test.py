from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

from tools.caldera_tools import (
    caldera_api_request,
    caldera_api_method_details,
    caldera_swagger_info,
)


config_list = config_list_from_json(env_or_file="OAI_CONFIG.json")
assistant = ConversableAgent(
    "assistant",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
)
user_proxy = ConversableAgent(
    "user_proxy",
    llm_config={"config_list": config_list},
    is_termination_msg=lambda msg: (
        msg["content"] and "goodbye" in msg["content"].lower()
    ),
    human_input_mode="NEVER",
)  # IMPORTANT: set to True to run code in docker, recommended

assistant.register_for_llm(
    name="caldera_swagger_info",
    description="Retrieve the list of all available Caldera API methods along with a description of their functionality",
)(caldera_swagger_info)

assistant.register_for_llm(
    name="caldera_api_method_details",
    description="Retrieve the details on a specific API method in Caldera including the parameters it takes and the responses it returns.",
)(caldera_api_method_details)

assistant.register_for_llm(
    name="caldera_api_request",
    description="Perform an API request to Caldera based on the given API method extracted from the Swagger documentation.",
)(caldera_api_request)

user_proxy.register_for_execution(name="caldera_swagger_info")(caldera_swagger_info)
user_proxy.register_for_execution(name="caldera_api_method_details")(
    caldera_api_method_details
)
user_proxy.register_for_execution(name="caldera_api_request")(caldera_api_request)

chat_result = user_proxy.initiate_chat(
    assistant,
    message="Find out which agent is running by talking to the Caldera API. Give name and paw, and finish by saying goodbye",
)
