import autogen.runtime_logging
from agents.ti_agent import ti_agent_user_proxy, ti_agent
from agents.human_agent import human_analyst_agent

from utils.shared_config import clean_working_directory, llm_config
import autogen


def run_scenario():
    clean_working_directory("/pdf")

    groupchat = autogen.GroupChat(
        agents=[
            human_analyst_agent,
            ti_agent_user_proxy,
            ti_agent,
        ],
        messages=[],
    )
    groupchat_manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    scenario_messages = [
        "Download the report from https://www.microsoft.com/en-us/security/blog/2024/04/22/analyzing-forest-blizzards-custom-post-compromise-tool-for-exploiting-cve-2022-38028-to-obtain-credentials/",
        "Analyze the threat intelligence report and provide a bullet-style list of the techniques used by the adversaries",
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
