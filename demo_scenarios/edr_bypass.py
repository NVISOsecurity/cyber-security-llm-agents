import autogen.runtime_logging
from agents.caldera_agent import caldera_agent_user_proxy, caldera_agent
from agents.human_agent import human_analyst_agent

from utils.shared_config import clean_working_directory, llm_config
import autogen


def run_scenario():
    clean_working_directory("/pdf")

    groupchat = autogen.GroupChat(
        agents=[
            human_analyst_agent,
            caldera_agent_user_proxy,
            caldera_agent,
        ],
        messages=[],
    )
    groupchat_manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    scenario_messages = [
        "Verify on the active Caldera agent if you are running privileged or not using Powershell. Get the Active Agent PAW from the Caldera API",
        "Summarize a list of techniques often used by adversaries to elevate privileges on Windows. Don't use ANY tools to do this. Be as specific as possible.",
        "Analyze the available flags at https://github.com/peass-ng/PEASS-ng/blob/master/winPEAS/winPEASexe/README.md",
        # "Check on the active Caldera agent which Windows services are running, and summarize them all in a table. Get the Active Agent PAW from the Caldera API",
        # "Download the list of all security products mentioned in https://github.com/tsale/EDR-Telemetry/blob/main/README.md",
        # "From the list of running services, identify the services that are EDR-related",
    ]

    scenario_messages = [
        "Get the ID of the active Caldera operation.",
        "Get the PAW of the active Caldera agent by calling /api/v2/agents.",
        "Summarize the ID and PAW from previous steps in a table.",
        "Use powershell to download http://192.168.162.11:8800/winPEASx86.exe  if it does not exist yet, and save it to C:\\temp of the active agent.",
        "Use powershell to run winPEASx86.exe to enumerate the system and save the output to C:\\temp.",
        # "Summarize the information available at https://book.hacktricks.xyz/windows-hardening/checklist-windows-privilege-escalation",
    ]

    for message in scenario_messages:
        # if first message, then clear history
        if message == scenario_messages[0]:
            clear_history = True
        else:
            clear_history = False

        chat_result = human_analyst_agent.initiate_chat(
            groupchat_manager,
            message=message,
            clear_history=clear_history,
        )
