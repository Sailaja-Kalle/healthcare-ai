# ChromaDB disabled for deployment - memory optimization
def get_chroma_client():
    return None

def get_or_create_collection(client=None, collection_name="medical_knowledge"):
    return None

def clear_collection(client=None, collection_name="medical_knowledge"):
    pass