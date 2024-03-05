import glob
import os
from dotenv import load_dotenv
from langchain.vectorstores.faiss import FAISS
from openai import AzureOpenAI
from utilities import config_utils

load_dotenv(verbose=True, override=True)


class LocalVectorstore(object):
    def __init__(self, knowledge_folder: str, vector_store_folder: str):
        self.knowledge_folder = knowledge_folder
        self.vector_store_folder = vector_store_folder
        self.create_vector_store()  # Create the vector store upon initialization
        self.VECTOR_STORE = self.load_vector_store()

    def create_vector_store(self):
        # Ensure the vector_store folder exists
        os.makedirs(self.vector_store_folder, exist_ok=True)

        # Load text files from the knowledge folder
        text_files = glob.glob(f"{self.knowledge_folder}/*.txt")

        # Initialize an empty FAISS vector store
        vector_store = FAISS()

        # Create embeddings for each text file and add them to the vector store
        for file_path in text_files:
            with open(file_path, "r") as file:
                text_content = file.read()
            # Create an embedding for the text content
            embedding = AzureOpenAI.embeddings.create(
                input=text_content, model=os.getenv("AZURE_EMBEDDINGS_MODEL_NAME", "")
            )
            # Add the embedding and the file path as metadata to the vector store
            vector_store.add([embedding.model_dump_json(indent=2)], [file_path])

        # Save the vector store locally in the vector_store_folder
        vector_store.save_local(
            folder_path=self.vector_store_folder, index_name="vector_store_index"
        )

    def load_vector_store(self) -> FAISS:
        # Get a list of all .faiss files in the vector store folder
        faiss_files = glob.glob(f"{self.vector_store_folder}/*.faiss")

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
                "No vector store found - check if the vector store folder contains at least one .faiss file!"
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


# Initialize the local vector store with the knowledge base folder path and vector store folder path
local_vector_store = LocalVectorstore(
    knowledge_folder="llm_knowledge_base", vector_store_folder="vector_store"
)
