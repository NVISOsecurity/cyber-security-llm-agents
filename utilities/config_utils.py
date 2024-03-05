import os

from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_core.utils import convert_to_secret_str
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv(verbose=True, override=True)

# Double dirname so we move 1 directory up, to the root
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the path to the text file relative to the script's directory
PROMPT_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, "prompts", "auto_api_caldera.txt")

with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as PROMPT_FILE:
    # Read the entire content of the file into a string
    GENERATE_COMMANDS_PROMPT = PROMPT_FILE.read()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()

AZURE_OPENAI_CLIENT = AzureOpenAI(
    azure_endpoint=os.getenv("OPENAI_API_BASE", ""),
    api_key=os.getenv("OPENAI_API_KEY", ""),
    api_version=os.getenv("OPENAI_API_VERSION", "2023-07-01-preview"),
)

AZURE_OPENAI_EMBEDDINGS = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("OPENAI_API_BASE", ""),
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME", ""),
    api_key=convert_to_secret_str(os.getenv("OPENAI_API_KEY", "")),
    api_version=os.getenv("OPENAI_API_VERSION", "2023-07-01-preview"),
)
