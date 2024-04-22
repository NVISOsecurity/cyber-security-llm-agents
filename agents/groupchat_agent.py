from autogen import AssistantAgent
from utils.shared_config import config_list

human_analyst_agent = AssistantAgent(
    "human_analyst_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"].upper(),
    description="A helpful agent that can help summarize, analyze and format text.",
    system_message="Output should always be analyzed or formatted text, and never source code",
)
