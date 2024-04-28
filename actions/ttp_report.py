import autogen.runtime_logging
from agents.ti_agent import ti_agent_user_proxy, ti_agent
from agents.analyst_agents import security_analyst_agent

from utils.shared_config import clean_working_directory, llm_config
import autogen


def run_scenario():
    clean_working_directory("/pdf")

    # from autogen.agentchat.contrib.capabilities import transforms, transform_messages
    # context_handling = transform_messages.TransformMessages(
    #    transforms=[
    #        transforms.MessageHistoryLimiter(max_messages=20),
    #         transforms.MessageTokenLimiter(
    #            max_tokens=utils.constants.MAX_TOKENS,
    #            max_tokens_per_message=utils.constants.MAX_TOKENS_PER_MESSAGE,
    #        ),
    #    ]
    # )

    groupchat = autogen.GroupChat(
        agents=[
            security_analyst_agent,
            ti_agent_user_proxy,
            ti_agent,
        ],
        messages=[],
    )
    groupchat_manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    scenario_messages = [
        "Download the PDF report from https://strapi.eurepoc.eu/uploads/Eu_Repo_C_APT_profile_APT_28_4856c0a0ac.pdf and provide a bullet-style list of the techniques used by the adversaries",
        "Extract a list of tools used by the adversaries from the report",
    ]

    for message in scenario_messages:
        # if first message, then clear history
        if message == scenario_messages[0]:
            clear_history = True
        else:
            clear_history = False

        chat_result = security_analyst_agent.initiate_chat(
            groupchat_manager,
            message=message,
            clear_history=clear_history,
        )
