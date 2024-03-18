from tools.subprocess_tool import SubprocessTool
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, PDFSearchTool
from utilities import logging_utils
import os
import json

docs_tool = DirectoryReadTool(directory="./threat-intelligence")
pdf_tool = PDFSearchTool(pdf="./threat-intelligence/TLP-CLEAR-CB-24-03.pdf")

subprocess_tool = SubprocessTool()

cmd_agent = Agent(
    role="Command-Line Process Analyst",
    goal="Run and analyze processes in a command-line shell to reach a goal",
    backstory="Your run in the context of a unix server",
)

cmd_task = Task(
    description=(
        "Analyze the output of the command-line process and extract the relevant information"
    ),
    agent=cmd_agent,
    expected_output="A list of users and their permissions",
    verbose=False,
)

# Load all the agents and tasks

# Initialize empty lists to store agents and tasks
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
                tools=[pdf_tool],
            )

            logging_utils.logger.info(f"Loaded agent: %s", agent_data["ID"])

            # Add the agent to the agents list
            agents.append(agent)

            # Create Task objects from the tasks in the JSON data
            for task_data in agent_data["tasks"]:
                task = Task(
                    description=task_data["description"],
                    expected_output=task_data["expected_output"],
                    verbose=True,
                )

                logging_utils.logger.info(f"Loaded task: %s", task_data["ID"])
                # Add the task to the tasks list
                tasks.append(task)


# Instantiate your crew with a sequential process
# crew = Crew(agents=[ti_agent], tasks=[ti_task], verbose=2)

# Get your crew to work!
# result = crew.kickoff()
