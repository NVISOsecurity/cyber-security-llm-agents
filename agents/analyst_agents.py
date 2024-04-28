from autogen import ConversableAgent
from utils.shared_config import config_list
from tools.web_tools import download_web_page

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
