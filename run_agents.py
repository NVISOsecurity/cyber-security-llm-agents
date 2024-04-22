import autogen.runtime_logging
from agents.caldera_agent import caldera_agent_user_proxy, caldera_agent
from utils.logs import print_usage_statistics
import autogen
import sys
import demo_scenarios.lsass, demo_scenarios.ttp_report

# context_handling.add_to_agent(human_analyst_agent)
# context_handling.add_to_agent(caldera_agent)

# Read flow to run from the first parameter
flow_to_run = sys.argv[1]

logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})

if flow_to_run == "lsass":
    demo_scenarios.lsass.run_scenario()
elif flow_to_run == "ttp_report":
    demo_scenarios.ttp_report.run_scenario()

autogen.runtime_logging.stop()
print_usage_statistics(logging_session_id)

exit()


chat_result = web_agent_user_proxy.initiate_chat(
    web_agent,
    message="Summarize the parameters available in the README.md file for tool https://raw.githubusercontent.com/fortra/nanodump/main/README.md. Include the parameter flag and a short description.",
    clear_history=False,
)

chat_result = caldera_agent_user_proxy.initiate_chat(
    caldera_agent,
    message="Use powershell to now dump lsass using nanodump and the summarized parameters, and output the results in C:\\temp",
    clear_history=False,
)

chat_result = caldera_agent_user_proxy.initiate_chat(
    caldera_agent,
    message="Run 'calc.exe' on the active agent for operation CalderaGPT. do NOT use abilities but links.",
    clear_history=True,
)

chat_result = web_agent_user_proxy.initiate_chat(
    web_agent,
    message="Summarize the parameters available in the README.md file for tool https://raw.githubusercontent.com/fortra/nanodump/main/README.md. Include the parameter flag and a short description.",
    clear_history=True,
)

chat_result = user_proxy_agent.initiate_chat(
    powershell_agent,
    message="Give me an example powershell command line to download and run nanodump in a one-liner, and save the output to a file.",
    clear_history=False,
)

chat_result = user_proxy_agent.initiate_chat(
    api_agent,
    message="Find out which agent is running by talking to the Caldera API. Give name and paw",
    clear_history=True,
)

chat_result = user_proxy_agent.initiate_chat(
    api_agent,
    message="Return the hostname string in reverse",
    clear_history=False,
)
