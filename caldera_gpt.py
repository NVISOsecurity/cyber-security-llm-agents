import sys
import json
import requests
import subprocess
from time import sleep
from utilities import gpt_utils, vector_store_utils

# Initialize the local vector store with the knowledge base folder path
local_vector_store = vector_store_utils.LocalVectorstore(
    knowledge_folder="llm_knowledge_base"
)

file_path = "prompts/auto_api_caldera.txt"
try:
    with open(file_path, "r") as file:
        file_content = file.read()
except FileNotFoundError:
    print(f"The file at {file_path} was not found.")
    sys.exit()

api_docs_url = "http://ubuntu-vm:8888/api/docs/swagger.json"
try:
    response = requests.get(api_docs_url)
    response.raise_for_status()
    api_docs_content = response.text
except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the API documentation: {e}")
    sys.exit()

updated_content = file_content.replace("<API_DOC_PLACEHOLDER>", api_docs_content)
steps_taken_placeholder = "<STEPS_TAKEN_PLACEHOLDER>"
steps_taken_history = []
completed = "no"

while completed.lower() != "yes":
    updated_content_with_history = updated_content.replace(
        steps_taken_placeholder, json.dumps(steps_taken_history, indent=2)
    )

    # Retrieve relevant snippets from the vector store to assist the model
    # Use the search_vector_store method from the LocalVectorstore instance
    search_results = local_vector_store.search_vector_store(
        updated_content_with_history, top_k=5  # Adjust top_k as needed
    )

    # Convert the search results into a format that can be appended to the prompt
    relevant_snippets_text = "\n".join(
        [result["metadata"] for result in search_results]
    )

    # Update the prompt with the relevant snippets
    updated_content_with_snippets = (
        updated_content_with_history
        + "\n\nRelevant Snippets:\n"
        + relevant_snippets_text
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
    print(f"Explanation: {explanation}")
    print(f"Completed: {completed}")

    sleep(10)
