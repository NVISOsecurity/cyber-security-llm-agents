import glob
import os
from dotenv import load_dotenv
from langchain.vectorstores.faiss import FAISS
from openai import AzureOpenAI
from utilities import config_utils

load_dotenv(verbose=True, override=True)


class LocalVectorstore(object):
    def __init__(self, knowledge_folder: str):
        self.knowledge_folder = knowledge_folder
        self.VECTOR_STORE = self.load_vector_store()

    def load_vector_store(self) -> FAISS:
        # Get a list of all .faiss files in the knowledge folder
        faiss_files = glob.glob(f"{self.knowledge_folder}/*.faiss")

        combined_faiss_vector_store = None

        # Loop over the list of .faiss files
        for file_path in faiss_files:
            index_folder = os.path.dirname(file_path)
            index_name = os.path.splitext(os.path.basename(file_path))[0]

            faiss_vector_store = FAISS.load_local(
                folder_path=index_folder,
                index_name=index_name,
                embeddings=config_utils.AZURE_OPENAI_EMBEDDINGS,
            )

            if combined_faiss_vector_store is None:
                combined_faiss_vector_store = faiss_vector_store
            else:
                combined_faiss_vector_store.merge_from(faiss_vector_store)

        if combined_faiss_vector_store is None:
            raise Exception(
                "No vector store found - check if the knowledge folder contains at least one .faiss file!"
            )

        return combined_faiss_vector_store

    def search_vector_store(self, query: str, top_k=5):
        # Search the vector store for the query
        embedding = AzureOpenAI.embeddings.create(
            input=query, model=os.getenv("AZURE_EMBEDDINGS_MODEL_NAME", "")
        )
        results = self.VECTOR_STORE.search(
            embedding.model_dump_json(indent=2), k=top_k, search_type="mmr"
        )
        return results


# Initialize the local vector store with the knowledge base folder path
local_vector_store = LocalVectorstore(knowledge_folder="llm_knowledge_base")
