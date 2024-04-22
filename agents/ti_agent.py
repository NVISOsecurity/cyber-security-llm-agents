from autogen import AssistantAgent
from utils.shared_config import config_list
from autogen import UserProxyAgent
from tools.web_tools import download_pdf_report

ti_agent = AssistantAgent(
    "ti_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    description="A helpful agent that can analyze threat intelligence information.",
)

ti_agent_user_proxy = UserProxyAgent(
    "ti_agent_user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
)

# Download PDF

ti_agent.register_for_llm(
    name="download_pdf_report",
    description="Download the content of a PDF report and return its content as a string.",
)(download_pdf_report)

ti_agent_user_proxy.register_for_execution(name="download_pdf_report")(
    download_pdf_report
)
