from autogen import UserProxyAgent, AssistantAgent
from utils.shared_config import config_list
import utils.constants

# create a UserProxyAgent instance named "user_proxy"
web_agent = AssistantAgent(
    name="web_agent",
    llm_config={"config_list": config_list},
)

web_agent_user_proxy = UserProxyAgent(
    name="web_agent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={
        "work_dir": utils.constants.LLM_WORKING_FOLDER + "/web",
        "use_docker": False,
    },
    llm_config={"config_list": config_list},
)
