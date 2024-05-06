actions = {
    "HELLO_AGENTS": [
        {"message": "Tell me a cyber security joke", "agent": "text_analyst_agent"}
    ],
    "SUMMARIZE_RECENT_CISA_VULNS": [
        {
            "message": """Run a single Shell command to download (using curl -sS) https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json,
            which is a JSON file containing an array of dictionaries. Filter out and print the last 10 JSON entries dictionaries using jq in the array under key 'vulnerabilities'.""",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the last 10 JSON entries dictionaries.",
            "agent": "cmd_exec_agent",
        },
        {
            "message": "Summarize the list of vulnerabilities by extracting the product name and a short description of each vulnerability, as well as link to more notes if available. Output as a table.",
            "summary_method": "reflection_with_llm",
            "agent": "text_analyst_agent",
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
    "TTP_REPORT_TO_ADVERSARY_PROFILE": [
        {
            "message": "Download the HTML report at https://thedfirreport.com/2024/04/29/from-icedid-to-dagon-locker-ransomware-in-29-days/ and extract the MITRE techniques.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with all the MITRE techniques extracted from the downloaded report.",
            "agent": "internet_agent",
        },
        {
            "message": "For each one of the MITRE techniques that was extracted from the report find a matching Caldera ability based on the technique id. Do not truncate the output.",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the matched Caldera abilities",
            "agent": "caldera_agent",
        },
        {
            "message": "Create a new adversary profile with an appropriate name according to the report contents and add one matched Caldera ability per technique",
            "summary_method": "last_msg",
            "carryover": "Replace this placeholder with the adversary profile information.",
            "agent": "caldera_agent",
        },
    ],
}

scenarios = {
    "HELLO_AGENTS": ["HELLO_AGENTS"],
    "SUMMARIZE_RECENT_CISA_VULNS": ["SUMMARIZE_RECENT_CISA_VULNS"],
    "HELLO_CALDERA": ["COLLECT_CALDERA_INFO", "HELLO_CALDERA"],
    "COLLECT_CALDERA_INFO": ["COLLECT_CALDERA_INFO"],
    "DETECT_EDR": ["COLLECT_CALDERA_INFO", "DETECT_EDR"],
    "DETECT_AGENT_PRIVILEGES": ["COLLECT_CALDERA_INFO", "DETECT_AGENT_PRIVILEGES"],
    "IDENTIFY_EDR_BYPASS_TECHNIQUES": ["IDENTIFY_EDR_BYPASS_TECHNIQUES"],
    "TTP_REPORT_TO_TECHNIQUES": ["TTP_REPORT_TO_TECHNIQUES"],
    "TTP_REPORT_TO_ADVERSARY_PROFILE": ["TTP_REPORT_TO_ADVERSARY_PROFILE"],
}
