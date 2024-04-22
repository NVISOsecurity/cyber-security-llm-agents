from agents.user_proxy_agent import user_proxy_agent
from agents.api_agent import api_agent
from agents.web_agent import web_agent, web_assistant
from agents.powershell_agent import powershell_agent
from utils.web_server import web_server_thread
from utils.shared_config import clean_working_directory

clean_working_directory()
web_server_thread.start()

# context_handling.add_to_agent(api_agent)
# context_handling.add_to_agent(web_agent)
# context_handling.add_to_agent(web_assistant)

chat_result = web_agent.initiate_chat(
    web_assistant,
    message="Summarize the command line parameters for https://github.com/fortra/nanodump by downloading & analyzing the readme",
    clear_history=True,
)

exit()

chat_result = user_proxy_agent.initiate_chat(
    powershell_agent,
    message="Give me an example powershell command line to download and run nanodump in a one-liner, and save the output to a file.",
    clear_history=False,
)

exit()

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
