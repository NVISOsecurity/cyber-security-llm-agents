from langchain_openai import ChatOpenAI
from tools.subprocess_tools import SubprocessTool
from crewai import Agent, Task, Process
from utilities import crew_utils, logging_utils, config_utils
from crewai import Crew
from tools.tools import tools_dict
import os
import json
import sys

subprocess_tool = SubprocessTool()

# Check if the command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: llm_agents.py <workflow_id>")
    sys.exit(1)

workflow_id = sys.argv[1]

workflow_agents = None
workflow_tasks = None

# Initialize empty lists to store agents and tasks
tools = []
agents = []
tasks = []
workflows = []

# Clear the progress file
with open(f"./{config_utils.LLM_WORKING_FOLDER}/progress.txt", "w") as f:
    f.write("")
    f.close()

# Loop through each file in the directory
for filename in os.listdir("agents"):
    if filename.endswith(".json"):
        file_path = os.path.join("agents", filename)

        # Read the JSON file
        with open(file_path, "r") as file:
            logging_utils.logger.info(f"Loading %s", file_path)

            agent_data = json.load(file)

            # Create an Agent object from the JSON data
            agent = Agent(
                role=agent_data["role"],
                goal=agent_data["goal"],
                backstory=agent_data["backstory"],
                verbose=config_utils.CREW_AGENT_DEBUGGING,
                memory=False,
                allow_delegation=False,
            )

            if "tools" in agent_data:
                agent_tools = [tools_dict[tool_str] for tool_str in agent_data["tools"]]
                agent.tools = agent_tools

            logging_utils.logger.info(f"\tLoaded agent: %s", agent_data["ID"])

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

                logging_utils.logger.info(f"\t\tLoaded task: %s", task_data["ID"])
                # Add the task to the tasks list
                tasks.append({"ID": task_data["ID"], "task": task})

# Now process all workflows
for filename in os.listdir("workflows"):
    if filename.endswith(".json"):
        file_path = os.path.join("workflows", filename)

        # Read the JSON file
        with open(file_path, "r") as file:
            logging_utils.logger.info(f"Loading %s", file_path)

            for workflow in json.load(file)["workflows"]:

                logging_utils.logger.info(f"\t\tLoaded workflow: %s", workflow["ID"])
                workflows.append(workflow)


workflow = next((wf for wf in workflows if wf["ID"] == workflow_id), None)

if workflow is None:
    print(f"Workflow '{workflow_id}' not found in {workflow_id}")
    sys.exit(1)

workflow_agents = [agent["agent"] for agent in agents]
workflow_tasks = [crew_utils.get_task(tasks, task_id) for task_id in workflow["tasks"]]

crew = Crew(
    agents=workflow_agents,
    tasks=workflow_tasks,
    share_crew=False,
    # process=Process.hierarchical,
    verbose=0,
    # manager_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125"),
)


# Get your crew to work!
result = crew.kickoff()
print(crew.usage_metrics)
