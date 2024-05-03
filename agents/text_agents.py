from autogen import ConversableAgent
from utils.shared_config import llm_config
from tools.web_tools import download_web_page, detect_telemetry_gaps
from agents.coordinator_agents import task_coordinator_agent

text_analyst_agent = ConversableAgent(
    name="text_analyst_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant that can analyze and summarize text.""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)

internet_agent = ConversableAgent(
    name="internet_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant that can assist in interacting with content on the internet.""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)


def register_tools():
    # Download a web page

    internet_agent.register_for_llm(
        name="download_web_page",
        description="Download the content of a web page and return it as a string. Only for text content such as markdown pages.",
    )(download_web_page)

    task_coordinator_agent.register_for_execution(name="download_web_page")(
        download_web_page
    )

    # Detect telemetry NOT detected by an EDR

    internet_agent.register_for_llm(
        name="detect_telemetry_gaps",
        description="Detect telemetry NOT detected by an EDR.",
    )(detect_telemetry_gaps)

    task_coordinator_agent.register_for_execution(name="detect_telemetry_gaps")(
        detect_telemetry_gaps
    )