import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from config.config import GOOGLE_API_KEY

EMBEDDINGS_DIR = "faiss_index"

def build_embeddings(documents):
    embedding_model = GoogleGenerativeAIEmbeddings(
        api_key=GOOGLE_API_KEY,
        model="models/embedding-001"  # Use the correct model
    )
    vector_store = FAISS.from_texts(documents, embedding_model)
    return vector_store

def save_embeddings(vector_store, dir_path=EMBEDDINGS_DIR):
    vector_store.save_local(dir_path)

def load_embeddings(dir_path=EMBEDDINGS_DIR):
    embedding_model = GoogleGenerativeAIEmbeddings(
        api_key=GOOGLE_API_KEY,
        model="models/embedding-001"
    )
    return FAISS.load_local(dir_path, embedding_model)

def initialize_embeddings(doc_folder="documents"):
    documents = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(doc_folder, filename), "r", encoding="utf-8") as f:
                documents.append(f.read())
    vector_store = build_embeddings(documents)
    save_embeddings(vector_store)
    return vector_store
