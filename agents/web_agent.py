from autogen import UserProxyAgent, AssistantAgent
from utils.shared_config import llm_config
from tools.web_tools import download_web_page

# create a UserProxyAgent instance named "user_proxy"
web_agent = AssistantAgent(
    name="web_agent",
    llm_config=llm_config,
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"].upper(),
    description="A helpful assistant designed to interact with and analyze web pages.",
)

web_agent_user_proxy = UserProxyAgent(
    name="web_agent_user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    # {
    #    "work_dir": utils.constants.LLM_WORKING_FOLDER + "/web",
    #    "use_docker": False,
    # },
)

web_agent.register_for_llm(
    name="download_web_page",
    description="Download the content of a web page and return it as a string.",
)(download_web_page)

web_agent_user_proxy.register_for_execution(name="download_web_page")(download_web_page)
