import os
from dotenv import load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

from utilities import config_utils
import glob

load_dotenv(verbose=True, override=True)


def _txt_string_to_docs(
    txt_string: str, file_metadata: dict[str, str]
) -> list[Document]:
    # Split the text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=4096, chunk_overlap=512)
    docs = splitter.create_documents([txt_string])

    # Add the file metadata to the doc specific metadata
    for doc in docs:
        doc.metadata |= file_metadata

    return docs


class LocalVectorstore(object):
    def __init__(self, knowledge_folder: str, vector_store_folder: str):
        self.knowledge_folder = knowledge_folder
        self.vector_store_folder = vector_store_folder
        self.vector_store_file = os.path.join(vector_store_folder, "index.faiss")

        if not os.path.exists(self.vector_store_file):
            self.create_vector_store()

        self.VECTOR_STORE = self.load_vector_store()

    def create_vector_store(self):
        combined_faiss_vector_store = None

        # Load text files from the knowledge folder
        text_files = glob.glob(f"{self.knowledge_folder}/*.txt")

        # Create embeddings for each text file and add them to the vector store
        for file_path in text_files:
            with open(file_path, "r") as file:
                text_content = file.read()

                docs = _txt_string_to_docs(
                    text_content, file_metadata={"file_path": file_path}
                )

                faiss_db = FAISS.from_documents(
                    documents=docs, embedding=config_utils.AZURE_OPENAI_EMBEDDINGS
                )

                if combined_faiss_vector_store is None:
                    combined_faiss_vector_store = faiss_db
                else:
                    combined_faiss_vector_store.merge_from(faiss_db)

        if combined_faiss_vector_store is not None:
            combined_faiss_vector_store.save_local(folder_path="vector_store")

    def load_vector_store(self) -> FAISS:
        return FAISS.load_local(
            self.vector_store_folder, embeddings=config_utils.AZURE_OPENAI_EMBEDDINGS
        )
