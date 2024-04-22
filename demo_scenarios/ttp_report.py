import autogen.runtime_logging
from agents.ti_agent import ti_agent_user_proxy, ti_agent
from agents.human_agent import human_analyst_agent

from utils.shared_config import clean_working_directory, llm_config
import autogen


def run_scenario():
    clean_working_directory("/caldera")

    groupchat = autogen.GroupChat(
        agents=[
            ti_agent_user_proxy,
            ti_agent,
        ],
        messages=[],
        speaker_selection_method="round_robin",
    )
    groupchat_manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    scenario_messages = [
        "Download the report from https://strapi.eurepoc.eu/uploads/Eu_Repo_C_APT_profile_APT_28_4856c0a0ac.pdf",
        "Analyze the report and provide a detailed overview of the TTP in table format. Include the MITRE technique ID, technique name and a small description how this is used by the adversary in different columns.",
    ]

    for message in scenario_messages:
        # if first message, then clear history
        if message == scenario_messages[0]:
            clear_history = True
        else:
            clear_history = False

        chat_result = ti_agent.initiate_chat(
            groupchat_manager,
            message=message,
            clear_history=clear_history,
        )
