from tools.subprocess_tools import SubprocessTool
from crewai import Agent, Task
from utilities import crew_utils, logging_utils
from crewai import Crew
from tools.tools import tools_dict
import os
import json


subprocess_tool = SubprocessTool()

# Load all the agents and tasks

# Initialize empty lists to store agents and tasks
tools = []
agents = []
tasks = []

# Loop through each file in the directory
for filename in os.listdir("agents"):
    if filename.endswith(".json"):
        file_path = os.path.join("agents", filename)

        # Read the JSON file
        with open(file_path, "r") as file:
            agent_data = json.load(file)

            # Create an Agent object from the JSON data
            agent = Agent(
                role=agent_data["role"],
                goal=agent_data["goal"],
                backstory=agent_data["backstory"],
            )

            logging_utils.logger.info(f"Loaded agent: %s", agent_data["ID"])

            # Add the agent to the agents list
            agents.append({"ID": agent_data["ID"], "agent": agent})

            # Create Task objects from the tasks in the JSON data
            for task_data in agent_data["tasks"]:
                task_tools = [tools_dict[tool_str] for tool_str in task_data["tools"]]

                task = Task(
                    description=task_data["description"],
                    expected_output=task_data["expected_output"],
                    tools=task_tools,
                    agent=agent,
                    verbose=False,
                )

                logging_utils.logger.info(f"Loaded task: %s", task_data["ID"])
                # Add the task to the tasks list
                tasks.append({"ID": task_data["ID"], "task": task})


# Instantiate your crew with a sequential process
crew = Crew(
    agents=[crew_utils.get_agent(agents, "cmd_line_analyst_agent")],
    tasks=[crew_utils.get_task(tasks, "system_health_check_task")],
    share_crew=False,
    verbose=0,
)

# Get your crew to work!
result = crew.kickoff()
print(crew.usage_metrics)
