from autogen import config_list_from_json
from autogen.agentchat.contrib.capabilities import transforms, transform_messages
from . import constants
import constants
import shutil
import os

# Get path to the script folder
script_folder = os.path.dirname(os.path.abspath(__file__))

# Get path to file "OAI_CONFIG.json"
config_file = os.path.join(script_folder, "../OAI_CONFIG.json")

config_list = config_list_from_json(env_or_file=config_file)

context_handling = transform_messages.TransformMessages(
    transforms=[
        # transforms.MessageHistoryLimiter(max_messages=10),
        transforms.MessageTokenLimiter(
            max_tokens=constants.MAX_TOKENS,
            max_tokens_per_message=constants.MAX_TOKENS_PER_MESSAGE,
        ),
    ]
)


def clean_working_directory():
    # Check if the folder exists
    if not os.path.exists(constants.LLM_WORKING_FOLDER):
        print(f"The folder {constants.LLM_WORKING_FOLDER} does not exist.")
        return

    # Loop through all the items in the folder
    for filename in os.listdir(constants.LLM_WORKING_FOLDER):
        file_path = os.path.join(constants.LLM_WORKING_FOLDER, filename)
        try:
            # If it's a file, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it's a directory, remove it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
