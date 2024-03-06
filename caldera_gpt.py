import sys
import json
import requests
import subprocess
from time import sleep
from utilities import gpt_utils, vector_store_utils, config_utils, logging_utils
from datetime import datetime

logging_utils.wipe_llm_interactions_file()

# Initialize the local vector store with the knowledge base folder path
local_vector_store = vector_store_utils.LocalVectorstore(
    knowledge_folder="llm_knowledge_base", vector_store_folder="vector_store"
)

prompt_template = config_utils.AUTO_API_CALDERA_PROMPT.replace(
    "<OBJECTIVE_PLACEHOLDER>",
    "change the background of any of the agents to the image at URL https://blog.nviso.eu/wp-content/uploads/2022/12/cropped-abn-zcrj_400x400-1.png.",
)

action_history_placeholder = "<ACTION_HISTORY_PLACEHOLDER>"
current_action_placeholder = "<CURRENT_ACTION_PLACEHOLDER>"
documentation_placeholder = "<DOCUMENTATION_PLACEHOLDER>"


actions = []
current_scenario = None
current_action = None

while current_scenario != 3:
    llm_prompt = None

    # Construct the truncated action history
    if len(actions) > 0:
        current_action = actions[-1]
        truncated_action_history = [
            {
                key: value
                for key, value in action_dict.items()
                if key != "command_output"
            }
            for action_dict in actions[:-1]
        ]
    else:
        truncated_action_history = []
        current_action = []

    # Construct the documentation snippets
    if current_scenario == 1:
        documentation_snippets = local_vector_store.VECTOR_STORE.search(
            json.dumps(current_action, indent=2), topk=5, search_type="mmr"
        )
    else:
        documentation_snippets = []

    # Now construct the entire prompt
    llm_prompt = (
        prompt_template.replace(
            action_history_placeholder, json.dumps(truncated_action_history, indent=2)
        )
        .replace(current_action_placeholder, json.dumps(current_action, indent=2))
        .replace(documentation_placeholder, str(documentation_snippets))
    )

    # Now pass the prompt to GPT
    gpt_output = json.loads(gpt_utils.run_llm_query(llm_prompt))

    # Update current scenario
    if "action" in gpt_output.keys():
        logging_utils.logger.info("")
        logging_utils.logger.info("====== New Action (LLM) ======")
        logging_utils.logger.info(gpt_output["action"])
        logging_utils.logger.info(
            "Documentation requested: " + gpt_output["need_documentation"]
        )
        current_scenario = 1
    if "command" in gpt_output.keys():
        logging_utils.logger.info("")
        logging_utils.logger.info("====== Command (LLM) ======")
        logging_utils.logger.info(gpt_output["command"])
        current_scenario = 2
    if "debrief" in gpt_output.keys():
        logging_utils.logger.info("")
        logging_utils.logger.info("====== Objective Reached (LLM) ======")
        logging_utils.logger.info(gpt_output["debrief"])
        current_scenario = 3

    if current_scenario == 1:
        actions.append(
            {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": gpt_output.get("action"),
            }
        )

    elif current_scenario == 2:
        command = gpt_output.get("command")
        try:
            command_output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True
            )
        except subprocess.CalledProcessError as e:
            command_output = e.output

        # Update the latest action in the history
        actions[-1] = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": actions[-1]["action"],
            "command": command,
            "command Output": command_output,
        }

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
