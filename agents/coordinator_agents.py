from autogen import ConversableAgent
from utils.shared_config import llm_config

task_coordinator_agent = ConversableAgent(
    name="task_coordinator_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant to solve tasks.""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)
