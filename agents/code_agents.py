from autogen import ConversableAgent
from utils.shared_config import llm_config
from agents.text_agents import task_coordinator_agent

from tools.code_tools import exec_shell_command


cmd_exec_agent = ConversableAgent(
    name="cmd_exec_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant that can execute commands to solve problems""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)


def register_tools():
    cmd_exec_agent.register_for_llm(
        name="exec_shell_command",
        description="Execute shell commands to solve tasks and problems",
    )(exec_shell_command)

    task_coordinator_agent.register_for_execution(name="exec_shell_command")(
        exec_shell_command
    )
