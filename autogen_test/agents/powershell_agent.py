from autogen import AssistantAgent
from utils.shared_config import config_list

powershell_agent = AssistantAgent(
    name="powershell_agent",
    llm_config={
        "config_list": config_list,
        "cache_seed": None,
    },
    description="This agent is designed to generate PowerShell commands. Its output can be directly used in a PowerShell terminal. It should ONLY output PowerShell commands.",
    system_message="Output should ONLY be PowerShell commands which can be directly used in a PowerShell terminal. Start command with 'powershell'.",
    max_consecutive_auto_reply=3,
)
