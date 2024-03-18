from tools.subprocess_tool import SubprocessTool
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_core.tools import BaseTool
from crewai_tools import DirectoryReadTool, FileReadTool, PDFSearchTool
from langchain_openai import AzureChatOpenAI
from langchain_core.utils import convert_to_secret_str

load_dotenv(verbose=True, override=True)

docs_tool = DirectoryReadTool(directory="./threat-intelligence")
pdf_tool = PDFSearchTool(pdf="./threat-intelligence/TLP-CLEAR-CB-24-03.pdf")

subprocess_tool = SubprocessTool()

cmd_agent = Agent(
    role="Command-Line Process Analyst",
    goal="Run and analyze processes in a command-line shell to reach a goal",
    backstory="Your run in the context of a unix server",
)

ti_agent = Agent(
    role="Threat Intelligence Analyst",
    goal="Gather intelligence on the latest threats and vulnerabilities",
    backstory="You are a security analyst",
    tools=[pdf_tool],
)

ti_task = Task(
    description=("Analyze the Threat Intelligence report"),
    agent=ti_agent,
    expected_output="generate a table of MITRE technique IDs and descriptions, \
            by interpreting the adversarial activities described in the incident report \
            and using your knowledge to describe them to TTPs. Include as columns the MITRE ID, \
            the technique name, and the name of the section of the document that mentions the \
            technique being used by adversaries.",
    verbose=False,
)

cmd_task = Task(
    description=(
        "Analyze the output of the command-line process and extract the relevant information"
    ),
    agent=cmd_agent,
    expected_output="A list of users and their permissions",
    verbose=False,
)

# Instantiate your crew with a sequential process
crew = Crew(agents=[ti_agent], tasks=[ti_task], verbose=2)

# Get your crew to work!
result = crew.kickoff()
