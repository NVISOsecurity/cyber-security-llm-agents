import os

from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

# Double dirname so we move 1 directory up, to the root
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the path to the text file relative to the script's directory
PROMPT_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, "prompts", "generate_commands.txt")

with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as PROMPT_FILE:
    # Read the entire content of the file into a string
    GENERATE_COMMANDS_PROMPT = PROMPT_FILE.read()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
