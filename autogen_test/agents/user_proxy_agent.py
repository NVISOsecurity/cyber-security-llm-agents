from autogen import UserProxyAgent
from tools.caldera_tools import (
    caldera_api_request,
    caldera_api_method_details,
    caldera_swagger_info,
)

user_proxy_agent = UserProxyAgent(
    "user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
)

user_proxy_agent.register_for_execution(name="caldera_swagger_info")(
    caldera_swagger_info
)
user_proxy_agent.register_for_execution(name="caldera_api_method_details")(
    caldera_api_method_details
)
user_proxy_agent.register_for_execution(name="caldera_api_request")(caldera_api_request)
