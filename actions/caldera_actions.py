actions = {
    "ALERT_KNOWN_EXPLOITED_CISA_VULNS": [
        {
            "message": "Prepare a cmd line command to download and print the last 50 lines of https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            "summary_method": "last_msg",
            "agent": "text_analyst_agent",
        },
        {
            "message": "Run the command",
            "summary_method": "last_msg",
            "agent": "cmd_execution_agent",
        },
    ],
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
    "TTP_REPORT_TO_TECHNIQUES": [
        {
            "message": "Download the HTML report at https://www.microsoft.com/en-us/security/blog/2024/04/22/analyzing-forest-blizzards-custom-post-compromise-tool-for-exploiting-cve-2022-38028-to-obtain-credentials/",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with all the MITRE techniques extracted from the downloaded report.",
            "agent": "internet_agent",
        }
    ],
}

scenarios = {
    "ALERT_KNOWN_EXPLOITED_CISA_VULNS": ["ALERT_KNOWN_EXPLOITED_CISA_VULNS"],
    "HELLO_CALDERA": ["COLLECT_CALDERA_INFO", "HELLO_CALDERA"],
    "COLLECT_CALDERA_INFO": ["COLLECT_CALDERA_INFO"],
    "DETECT_EDR": ["COLLECT_CALDERA_INFO", "DETECT_EDR"],
    "DETECT_AGENT_PRIVILEGES": ["COLLECT_CALDERA_INFO", "DETECT_AGENT_PRIVILEGES"],
    "IDENTIFY_EDR_BYPASS_TECHNIQUES": ["IDENTIFY_EDR_BYPASS_TECHNIQUES"],
    "TTP_REPORT_TO_TECHNIQUES": ["TTP_REPORT_TO_TECHNIQUES"],
}
