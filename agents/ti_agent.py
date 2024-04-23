from utils.shared_config import config_list
from autogen import ConversableAgent
from tools.web_tools import download_pdf_report
from tools.web_tools import download_web_page

ti_agent = ConversableAgent(
    "ti_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower()
    or "feel free to" in msg["content"].lower(),
    description="A helpful agent that can analyze threat intelligence information.",
    system_message="Include TERMINATE in the message when you want to stop the conversation.",
)

ti_agent_user_proxy = ConversableAgent(
    "ti_agent_user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
)

# Download PDF

ti_agent.register_for_llm(
    name="download_pdf_report",
    description="Download the content of a PDF report and return its content as a string.",
)(download_pdf_report)

ti_agent_user_proxy.register_for_execution(name="download_pdf_report")(
    download_pdf_report
)

# Download web page

ti_agent.register_for_llm(
    name="download_web_page",
    description="Download the content of a web page and return it as a string. Only for text content such as markdown pages.",
)(download_web_page)

ti_agent_user_proxy.register_for_execution(name="download_web_page")(download_web_page)
