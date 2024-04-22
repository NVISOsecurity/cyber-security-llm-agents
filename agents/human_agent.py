from autogen import AssistantAgent
from utils.shared_config import config_list

human_analyst_agent = AssistantAgent(
    "human_analyst_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    description="A helpful agent that can help summarize, analyze and format text",
)
