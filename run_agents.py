import autogen.runtime_logging
from agents import caldera_agents
from agents import analyst_agents
from utils.logs import print_usage_statistics
import autogen
import sys
import actions.caldera_actions
from agents.analyst_agents import (
    security_analyst_agent,
    task_coordinator_agent,
    text_analyst_agent,
)
from utils.shared_config import clean_working_directory
import actions.caldera_actions
from utils.shared_config import llm_config


def main():
    clean_working_directory("/caldera")
    clean_working_directory("/pdf")

    # Register tools
    caldera_agents.register_tools()
    analyst_agents.register_tools()

    # Read flow to run from the first parameter
    scenario_to_run = sys.argv[1]

    scenario_agents = []
    scenario_messages = []

    if scenario_to_run in actions.caldera_actions.scenarios.keys():
        scenario_action_names = actions.caldera_actions.scenarios[scenario_to_run]

        for scenario_action_name in scenario_action_names:
            for scenario_action in actions.caldera_actions.actions[
                scenario_action_name
            ]:
                scenario_agents.append(scenario_action["agent"])
                scenario_messages.append(scenario_action["message"])

    if scenario_messages:
        logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
        run_scenario(scenario_agents, scenario_messages)
        autogen.runtime_logging.stop()
        print_usage_statistics(logging_session_id)
    else:
        print("Scenario not found, exiting")


def run_scenario(scenario_agents, scenario_messages):
    for task_agent, task_message in zip(scenario_agents, scenario_messages):
        chat_results = task_coordinator_agent.initiate_chats(
            [
                {
                    "recipient": task_agent,
                    "message": task_message,
                    "clear_history": False,
                    "silent": False,
                    "summary_method": "last_msg",  # reflection_with_llm
                }
            ]
        )


if __name__ == "__main__":
    main()
