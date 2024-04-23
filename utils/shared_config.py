from autogen import config_list_from_json
import utils.constants
import shutil
import os

# Get path to the script folder
script_folder = os.path.dirname(os.path.abspath(__file__))

# Get path to file "OAI_CONFIG.json"
config_file = os.path.join(script_folder, "../OAI_CONFIG.json")
config_list = config_list_from_json(env_or_file=config_file)
llm_config = {"config_list": config_list, "cache_seed": None}


def clean_working_directory(agent_subfolder: str):
    # Check if the folder exists
    folder = utils.constants.LLM_WORKING_FOLDER + agent_subfolder

    # Avoid accidental deletion of the root folder
    if folder == "":
        print("Cannot delete the root folder.")
        return

    if not os.path.exists(folder):
        print(f"The folder {folder} does not exist.")
        return

    # Loop through all the items in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            # If it's a file, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it's a directory, remove it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
