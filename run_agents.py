import autogen.runtime_logging
from utils.logs import print_usage_statistics
import autogen
import sys
import actions.caldera_actions, actions.ttp_report, actions.edr_bypass
from utils.shared_config import clean_working_directory
import actions.caldera_actions
from utils.shared_config import llm_config


def main():
    clean_working_directory("/caldera")
    clean_working_directory("/pdf")

    # Read flow to run from the first parameter
    scenario_to_run = sys.argv[1]

    scenario_agents = []
    scenario_messages = []

    # Red Teaming scenarios
    if scenario_to_run in actions.caldera_actions.scenarios.keys():
        scenario_action_names = actions.caldera_actions.scenarios[scenario_to_run]

        for scenario_action_name in scenario_action_names:
            scenario_action = actions.caldera_actions.actions[scenario_action_name]
            scenario_agents.extend(scenario_action["agents"])
            scenario_messages.extend(scenario_action["messages"])

    if scenario_messages and scenario_agents:
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
        # if first message, then clear history
        if scenario_message == scenario_messages[0]:
            clear_history = True
        else:
            clear_history = False

        chat_result = scenario_agents[0].initiate_chat(
            groupchat_manager,
            message=scenario_message,
            clear_history=clear_history,
        )


if __name__ == "__main__":
    main()
