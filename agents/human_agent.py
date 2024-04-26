from autogen import ConversableAgent, UserProxyAgent
from utils.shared_config import config_list
from tools.web_tools import download_web_page

human_analyst_agent = ConversableAgent(
    "human_analyst_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower()
    or "feel free to" in msg["content"].lower(),
    description="A helpful human assistant that is useful for general purpose tasks. Never generates or executes code.",
    system_message="Include TERMINATE in the message when you want to stop the conversation.",
)

human_agent_user_proxy = ConversableAgent(
    "human_agent_user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
    llm_config={"config_list": config_list},
    default_auto_reply="Nothing to report, as I did not perform any actions in this round.",
    max_consecutive_auto_reply=5,
)

# Download a web page

human_analyst_agent.register_for_llm(
    name="download_web_page",
    description="Download the content of a web page and return it as a string. Only for text content such as markdown pages.",
)(download_web_page)

human_agent_user_proxy.register_for_execution(name="download_web_page")(
    download_web_page
)
