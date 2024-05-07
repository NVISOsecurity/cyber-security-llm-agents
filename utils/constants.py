import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Initialize the variables
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")
MAX_TOKENS = os.getenv("MAX_TOKENS")
MAX_TOKENS_PER_MESSAGE = os.getenv("MAX_TOKENS_PER_MESSAGE")
LLM_WORKING_FOLDER = os.getenv("LLM_WORKING_FOLDER", "llm_working_folder")

FTP_SERVER_ADDRESS = os.getenv("FTP_SERVER_ADDRESS")
FTP_SERVER_USER = os.getenv("FTP_SERVER_USER")
FTP_SERVER_PASS = os.getenv("FTP_SERVER_PASS")

CALDERA_SERVER = os.getenv("CALDERA_SERVER")
CALDERA_API_KEY = os.getenv("CALDERA_API_KEY")

OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Optionally, convert string values to the appropriate type if needed (e.g., integers)
WEB_SERVER_PORT = int(WEB_SERVER_PORT) if WEB_SERVER_PORT else 8800
MAX_TOKENS = int(MAX_TOKENS) if MAX_TOKENS else None
MAX_TOKENS_PER_MESSAGE = int(MAX_TOKENS_PER_MESSAGE) if MAX_TOKENS_PER_MESSAGE else None
