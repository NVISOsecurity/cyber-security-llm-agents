import sys
import json
import requests
import subprocess
from time import sleep
from utilities import gpt_utils, vector_store_utils, config_utils, logging_utils
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: caldera_gpt.py <OBJECTIVE>")
    sys.exit(1)


logging_utils.wipe_llm_interactions_file()

# Initialize the local vector store with the knowledge base folder path
local_vector_store = vector_store_utils.LocalVectorstore(
    knowledge_folder="llm_knowledge_base", vector_store_folder="vector_store"
)

objective = sys.argv[1]

prompt_template = config_utils.AUTO_API_CALDERA_PROMPT.replace(
    "<OBJECTIVE_PLACEHOLDER>",
    objective,
)

action_history_placeholder = "<ACTION_HISTORY_PLACEHOLDER>"
current_action_placeholder = "<CURRENT_ACTION_PLACEHOLDER>"
documentation_placeholder = "<DOCUMENTATION_PLACEHOLDER>"

actions = []
current_scenario = None
current_action = []

need_documentation = False
status = "busy"

logging_utils.logger.info("")
logging_utils.logger.info("====== Objective: %s ======", objective)
logging_utils.logger.info("")

while status != "finished":
    llm_prompt = None

    # Construct the documentation snippets
    if need_documentation:
        documentation_documents = local_vector_store.VECTOR_STORE.search(
            json.dumps(need_documentation, indent=2), topk=5, search_type="mmr"
        )

        documentation_snippets = []
        for doc in documentation_documents:
            documentation_snippets.append(doc.page_content)
    else:
        documentation_snippets = []

    documentation_snippets = "Not supported for now"

    # Now construct the entire prompt
    llm_prompt = (
        prompt_template.replace(
            action_history_placeholder, json.dumps(actions, indent=2)
        )
        .replace(current_action_placeholder, json.dumps(current_action, indent=2))
        .replace(documentation_placeholder, str(documentation_snippets))
    )

    # Now pass the prompt to GPT
    gpt_output = json.loads(gpt_utils.run_llm_query(llm_prompt))

    # Process all GPT output fields
    action = gpt_output.get("action")
    status = gpt_output.get("status")
    reasoning = gpt_output.get("reasoning")

    command = gpt_output.get("command", None)
    need_documentation = gpt_output.get("need_documentation", None)
    action_result = gpt_output.get("action_result", None)

    command_output = None
    if command:
        try:
            command_output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True
            )

            try:
                command_output = json.dumps(json.loads(command_output), indent=2)
            except json.JSONDecodeError:
                pass

            # Truncate output to X characters
            # Add a note of the number of truncated characters too
            if len(command_output) > 10000:
                command_output = (
                    command_output[:10000]
                    + f"\n... and {len(command_output) - 10000} more characters, truncated command output"
                )

        except subprocess.CalledProcessError as e:
            command_output = e.output

    logging_utils.logger.info("")

    if actions and actions[-1]["action"] == action:
        logging_utils.logger.info("====== Existing Action (LLM): %s ======", action)
        # Update the fields of the last action
        actions[-1].update(
            {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": status,
                "reasoning": reasoning,
                "need_documentation": need_documentation,
                "command": command,
                "command_output": command_output,
                "action_result": action_result,
            }
        )
    else:
        logging_utils.logger.info("====== New Action (LLM): %s ======", action)
        # Append a new action if it's not a match or if the actions list is empty
        actions.append(
            {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": action,
                "status": status,
                "reasoning": reasoning,
                "need_documentation": need_documentation,
                "command": command,
                "command_output": command_output,
                "action_result": action_result,
            }
        )

    # Remove all keys for which the value is None
    actions[-1] = {k: v for k, v in actions[-1].items() if v is not None}

    logging_utils.logger.info("Status: " + status)
    logging_utils.logger.info("Reasoning: " + reasoning)
    if command:
        logging_utils.logger.info("Command: " + gpt_output["command"])
        logging_utils.logger.info(
            "Command Output: " + str(command_output)[:200] + "..."
        )

    if action_result:
        logging_utils.logger.info("Action Result: " + str(gpt_output["action_result"]))
    if need_documentation:
        logging_utils.logger.info(
            "Documentation requested: " + gpt_output["need_documentation"]
        )

    if llm_prompt:
        with open("debug/llm_interactions.txt", "a") as file:
            file.write(llm_prompt.split("---------------------------", 1)[1])

            file.write("\n\n")
            file.write("============")
            file.write("LLM RESPONSE")
            file.write("============")
            file.write("\n\n")

            file.write(json.dumps(gpt_output, indent=2))
            file.write("\n\n" + "XXXXX" * 100 + "\n\n")

    sleep(1)
