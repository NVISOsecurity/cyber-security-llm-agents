from tools.subprocess_tools import SubprocessTool
from crewai import Agent, Task
from utilities import crew_utils, logging_utils, config_utils
from crewai import Crew
from tools.tools import tools_dict
import os
import json
import sys


subprocess_tool = SubprocessTool()

# Check if the command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: run_workflow.py <workflow_id>")
    sys.exit(1)

workflow_id = sys.argv[1]

workflow_agents = None
workflow_tasks = None

# Initialize empty lists to store agents and tasks
tools = []
agents = []
tasks = []
workflows = []

# Wipe the agent action log
crew_utils.wipe_agent_action_log()

# Loop through each file in the directory
for filename in os.listdir("agents"):
    if filename.endswith(".json"):
        file_path = os.path.join("agents", filename)

        # Read the JSON file
        with open(file_path, "r") as file:
            logging_utils.logger.debug(f"Loading %s", file_path)

            agent_data = json.load(file)

            # Create an Agent object from the JSON data
            agent = Agent(
                role=agent_data["role"],
                goal=agent_data["goal"],
                backstory=agent_data["backstory"],
                verbose=config_utils.CREW_AGENT_DEBUGGING,
                memory=True,
                allow_delegation=False,
                step_callback=crew_utils.log_agent_action,
            )

            if "tools" in agent_data:
                agent_tools = [tools_dict[tool_str] for tool_str in agent_data["tools"]]
                agent.tools = agent_tools

            logging_utils.logger.debug(f"\tLoaded agent: %s", agent_data["ID"])

            # Add the agent to the agents list
            agents.append({"ID": agent_data["ID"], "agent": agent})

            # Create Task objects from the tasks in the JSON data
            for task_data in agent_data["tasks"]:
                task = Task(
                    description=task_data["description"],
                    expected_output=task_data["expected_output"],
                    agent=agent,
                    async_execution=False,
                    verbose=config_utils.CREW_TASK_DEBUGGING,
                )

                if "tools" in task_data:
                    task_tools = [
                        tools_dict[tool_str] for tool_str in task_data["tools"]
                    ]
                    task.tools = task_tools

                logging_utils.logger.debug(f"\t\tLoaded task: %s", task_data["ID"])
                # Add the task to the tasks list
                tasks.append({"ID": task_data["ID"], "task": task})

# Now process all workflows
for filename in os.listdir("workflows"):
    if filename.endswith(".json"):
        file_path = os.path.join("workflows", filename)

        # Read the JSON file
        with open(file_path, "r") as file:
            logging_utils.logger.debug(f"Loading %s", file_path)

            for workflow in json.load(file)["workflows"]:
                logging_utils.logger.debug(f"\t\tLoaded workflow: %s", workflow["ID"])
                workflows.append(workflow)


workflow = next((wf for wf in workflows if wf["ID"] == workflow_id), None)

if workflow is None:
    print(f"Workflow '{workflow_id}' not found")
    sys.exit(1)

workflow_agents = [agent["agent"] for agent in agents]
workflow_tasks = [crew_utils.get_task(tasks, task_id) for task_id in workflow["tasks"]]

agent_history_preamble = " Never try the same thing twice, and include information on what you will do different in your reasoning. Previous actions you took: \n\n "
agent_action_log = None

for task in workflow_tasks:
    task_succeeded = False

    while not task_succeeded:
        if agent_action_log:
            for agent in workflow_agents:
                # Remove all the text from the preamble and onward from the backstory
                preamble_start = agent.backstory.find(agent_history_preamble)
                if preamble_start != -1:
                    agent.backstory = agent.backstory[:preamble_start]

                # Now update the backstory again with the action history
                agent.backstory = (
                    agent.backstory
                    + agent_history_preamble
                    + crew_utils.truncate_output_beginning(agent_action_log)
                )

                print(agent.backstory)

        crew = Crew(
            agents=workflow_agents,
            tasks=[task],
            share_crew=False,
            verbose=0,
        )

        result = crew.kickoff()
        logging_utils.logger.info(crew.usage_metrics)

        agent_action_log = crew_utils.agent_action_log()

        # Find the last occurrence of TASK_FAILED and TASK_SUCCEEDED
        last_failed = agent_action_log.rfind("TASK_FAILED")
        last_succeeded = agent_action_log.rfind("TASK_SUCCEEDED")

        if last_succeeded > last_failed:
            task_succeeded = True
            logging_utils.logger.info("Last task succeeded, moving to the next one!")
        else:
            logging_utils.logger.info("Task failed, retrying...")
