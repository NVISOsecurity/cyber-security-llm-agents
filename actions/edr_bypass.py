import autogen.runtime_logging
from agents.text_agents import human_analyst_agent

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
        "Get the ID of the active Caldera operation.",
        "Get the PAW of the active Caldera agent by calling /api/v2/agents.",
        """Get the list of services running on the active Caldera agent and return the raw command results.
        Filter out ALL services that contain the word 'WINDOWS' in their path and filter out ALL services that have quotes in their pathname.
        Output ALL the filtered results (do NOT summarize - this is VERY important) as table with name and path.""",
        "List all the security agents that are running on the system",
        # """Check on the active Caldera agent which Windows services of are running in their PathName.
        # Analyze the output and keep ONLY the ones for with the PathName,
        # and where PathName is NOT surrounded by quotes and for which the PathName does NOT contain WINDOWS.
        # The PathName should also NOT be empty.
        # Output the PathName and the Name as a table.
        # """
        #         "Summarize a list of techniques often used by adversaries to elevate privileges on Windows. Don't use ANY tools to do this. Be as specific as possible.",
        # "Use powershell to download http://192.168.162.11:8800/winPEASx86.exe if it does not exist yet, and save it to C:\\temp of the active agent.",
        # "Use powershell to run winPEASx86.exe to enumerate the system and save the output to C:\\temp.",
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
