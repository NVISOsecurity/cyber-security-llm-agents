import utils.constants
import shutil
import os

# Get path to the script folder
script_folder = os.path.dirname(os.path.abspath(__file__))
working_folder = os.path.join(script_folder, "../" + utils.constants.LLM_WORKING_FOLDER)
llm_config = {
    "model": utils.constants.OPENAI_MODEL_NAME,
    "api_key": utils.constants.OPENAI_API_KEY,
    "cache_seed": None,
}


def clean_working_directory(agent_subfolder: str):
    # Check if the folder exists
    working_subfolder = working_folder + agent_subfolder

    # Avoid accidental deletion of the root folder
    if working_subfolder == "":
        print("Cannot delete the root folder.")
        return

    if not os.path.exists(working_subfolder):
        print(f"The folder {working_subfolder} does not exist.")
        return

    # Loop through all the items in the folder
    for filename in os.listdir(working_subfolder):
        file_path = os.path.join(working_subfolder, filename)
        try:
            # If it's a file, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it's a directory, remove it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
