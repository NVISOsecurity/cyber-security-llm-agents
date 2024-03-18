import os

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from openai import AzureOpenAI

load_dotenv(verbose=True, override=True)

# Double dirname so we move 1 directory up, to the root
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()

AZURE_OPENAI_EMBEDDINGS = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT", ""),
    api_key=os.getenv("OPENAI_AZURE_API_KEY", ""),
    api_version=os.getenv("OPENAI_API_VERSION", "2023-07-01-preview"),
    azure_deployment=os.getenv("AZURE_EMBEDDINGS_MODEL_NAME", ""),
)

AZURE_OPENAI_CHAT_CLIENT = AzureChatOpenAI(
    azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT", ""),
    azure_deployment=os.getenv("OPENAI_INFERENCE_MODEL_NAME", ""),
    api_key=os.getenv("OPENAI_AZURE_API_KEY", ""),
    api_version=os.getenv("OPENAI_API_VERSION", "2023-07-01-preview"),
)

AZURE_OPENAI_CLIENT = AzureOpenAI(
    azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT", ""),
    api_key=os.getenv("OPENAI_AZURE_API_KEY", ""),
    api_version=os.getenv("OPENAI_API_VERSION", "2023-07-01-preview"),
)
