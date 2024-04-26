import autogen.runtime_logging
from agents.caldera_agent import caldera_agent, caldera_agent_user_proxy
from utils.logs import print_usage_statistics
import autogen
import sys
import actions.caldera_actions, actions.ttp_report, actions.edr_bypass
from agents.human_agent import human_analyst_agent
from utils.shared_config import clean_working_directory
import actions.caldera_actions
from utils.shared_config import llm_config


def main():
    clean_working_directory("/caldera")
    clean_working_directory("/pdf")

    # Read flow to run from the first parameter
    scenario_to_run = sys.argv[1]

    scenario_agents = [human_analyst_agent]
    scenario_messages = []

    if scenario_to_run in actions.caldera_actions.scenarios.keys():
        scenario_action_names = actions.caldera_actions.scenarios[scenario_to_run]

        for scenario_action_name in scenario_action_names:
            scenario_action = actions.caldera_actions.actions[scenario_action_name]
            scenario_agents.extend(scenario_action["agents"])
            scenario_messages.extend(scenario_action["messages"])

    if scenario_messages:
        logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
        run_scenario(list(set(scenario_agents)), scenario_messages)
        autogen.runtime_logging.stop()
        print_usage_statistics(logging_session_id)
    else:
        print("Scenario not found, exiting")


def run_scenario(scenario_agents, scenario_messages):
    groupchat = autogen.GroupChat(
        agents=scenario_agents,
        messages=[],
        allow_repeat_speaker=False,
    )
    groupchat_manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    for scenario_message in scenario_messages:
        chat_result = caldera_agent.initiate_chat(
            caldera_agent_user_proxy,
            message=scenario_message,
            clear_history=False,
        )


if __name__ == "__main__":
    main()
