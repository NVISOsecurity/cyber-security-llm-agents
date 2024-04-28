from readline import clear_history
import autogen.runtime_logging
from agents import text_agents, caldera_agents
from utils.logs import print_usage_statistics
import autogen
import sys
import actions.caldera_actions
from agents.text_agents import (
    task_coordinator_agent,
)
from utils.shared_config import clean_working_directory
import actions.caldera_actions


def main():
    clean_working_directory("/caldera")
    clean_working_directory("/pdf")

    # Register tools
    text_agents.register_tools()
    caldera_agents.register_tools()

    # Read flow to run from the first parameter
    scenario_to_run = sys.argv[1]

    scenario_agents = []
    scenario_messages = []

    scenario_tasks = []

    if scenario_to_run in actions.caldera_actions.scenarios.keys():
        scenario_action_names = actions.caldera_actions.scenarios[scenario_to_run]

        for scenario_action_name in scenario_action_names:
            for scenario_action in actions.caldera_actions.actions[
                scenario_action_name
            ]:
                scenario_agents.append(scenario_action["agent"])
                scenario_messages.append(scenario_action["message"])

                scenario_task = {
                    "recipient": scenario_action["agent"],
                    "message": scenario_action["message"],
                    "clear_history": True,
                    "silent": False,
                }

                # if len(scenario_tasks) == 0:
                #    scenario_task["clear_history"] = True
                # else:
                #    scenario_task["clear_history"] = False

                if "summary_prompt" in scenario_action:
                    scenario_task["summary_prompt"] = scenario_action["summary_prompt"]

                if "summary_method" in scenario_action:
                    scenario_task["summary_method"] = scenario_action["summary_method"]

                if "carryover" in scenario_action:
                    scenario_task["carryover"] = scenario_action["carryover"]

                scenario_tasks.append(scenario_task)

    if scenario_messages:
        logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
        run_scenario(scenario_tasks)
        autogen.runtime_logging.stop()
        print_usage_statistics(logging_session_id)
    else:
        print("Scenario not found, exiting")


def run_scenario(scenario_tasks):
    chat_results = task_coordinator_agent.initiate_chats(scenario_tasks)


if __name__ == "__main__":
    main()
