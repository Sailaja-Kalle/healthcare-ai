import chromadb
from chromadb.config import Settings
import os

# Persistent ChromaDB storage
CHROMA_DB_PATH = "./rag/chroma_db"

def get_chroma_client():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    return client

def get_or_create_collection(client, collection_name="medical_knowledge"):
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def clear_collection(client, collection_name="medical_knowledge"):
    try:
        client.delete_collection(collection_name)
        print(f"Collection {collection_name} cleared.")
    except:
        pass