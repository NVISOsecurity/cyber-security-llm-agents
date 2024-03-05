import sys
import json
import requests
import subprocess
from time import sleep
from utilities import gpt_utils, vector_store_utils, config_utils

# Initialize the local vector store with the knowledge base folder path
local_vector_store = vector_store_utils.LocalVectorstore(
    knowledge_folder="llm_knowledge_base", vector_store_folder="vector_store"
)

# gpt_output = json.loads(
#    gpt_utils.run_llm_query(
#        "Execute calc.exe in every agent currently running.",
#        local_vector_store.VECTOR_STORE,
#    )
# )

file_path = "prompts/auto_api_caldera.txt"
try:
    with open(file_path, "r") as file:
        prompt = file.read()
except FileNotFoundError:
    print(f"The file at {file_path} was not found.")
    sys.exit()

prompt = prompt.replace(
    "<OBJECTIVE_PLACEHOLDER>", "List the names of every running agent."
)
steps_taken_placeholder = "<STEPS_TAKEN_PLACEHOLDER>"
steps_taken_history = []
completed = "no"

while completed.lower() != "yes":
    updated_content_with_history = prompt.replace(
        steps_taken_placeholder, json.dumps(steps_taken_history, indent=2)
    )

    # Retrieve relevant snippets from the vector store to assist the model
    # Use the search_vector_store method from the LocalVectorstore instance
    search_results = local_vector_store.VECTOR_STORE.search(
        updated_content_with_history, topk=5, search_type="mmr"
    )

    # Convert the search results into a format that can be appended to the prompt
    # relevant_snippets_text = "\n".join([result for result in search_results])

    # Update the prompt with the relevant snippets
    updated_content_with_snippets = (
        updated_content_with_history + "\n\nRelevant Snippets:\n" + str(search_results)
    )

    # Send the updated content to the GPT model and get the output
    gpt_output = json.loads(gpt_utils.run_llm_query(updated_content_with_snippets))

    command = gpt_output.get("command")
    explanation = gpt_output.get("explanation")
    completed = gpt_output.get("completed", "no")

    try:
        command_output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        command_output = e.output

    steps_taken_history.append(
        {
            "command": command,
            "explanation": explanation,
            "command_output": command_output,
            "completed": completed,
        }
    )

    print(f"Command: {command}")
    print(f"Output: {command_output}")
    print(f"Explanation: {explanation}")
    print(f"Completed: {completed}")

    sleep(10)
