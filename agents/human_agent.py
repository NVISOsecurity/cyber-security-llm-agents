from autogen import ConversableAgent
from utils.shared_config import config_list

human_analyst_agent = ConversableAgent(
    "human_analyst_agent",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    description="A helpful agent that is useful for general purpose tasks. Never generates or executes code",
)
