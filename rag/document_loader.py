from rag.medical_knowledge import MEDICAL_KNOWLEDGE
from rag.chroma_manager import get_chroma_client, get_or_create_collection

def load_knowledge_to_chromadb():
    """Load all medical knowledge into ChromaDB"""
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    # Check if already loaded
    existing = collection.count()
    if existing >= len(MEDICAL_KNOWLEDGE):
        print(f"✅ Knowledge already loaded: {existing} documents")
        return collection

    print(f"📚 Loading {len(MEDICAL_KNOWLEDGE)} documents into ChromaDB...")

    # Prepare data
    documents = []
    ids = []
    metadatas = []

    for item in MEDICAL_KNOWLEDGE:
        documents.append(item["text"])
        ids.append(item["id"])
        metadatas.append({"category": item["category"]})

    # Add to ChromaDB (uses built-in embeddings)
    collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    print(f"✅ Successfully loaded {len(MEDICAL_KNOWLEDGE)} documents!")
    return collection


def get_collection():
    """Get existing collection"""
    client = get_chroma_client()
    return get_or_create_collection(client)