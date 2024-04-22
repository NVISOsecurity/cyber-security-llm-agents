from autogen import UserProxyAgent, AssistantAgent
from utils.shared_config import config_list

# create a UserProxyAgent instance named "user_proxy"
web_assistant = AssistantAgent(
    name="web_assistant",
    llm_config={"config_list": config_list},
)

web_agent = UserProxyAgent(
    name="web_agent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={
        "work_dir": "llm_working_dir/web",
        "use_docker": False,
    },
    llm_config={"config_list": config_list},
)
