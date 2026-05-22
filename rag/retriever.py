from rag.document_loader import load_knowledge_to_chromadb, get_collection

def retrieve_relevant_docs(query, n_results=4, category_filter=None):
    """Retrieve most relevant documents for a query"""
    try:
        collection = load_knowledge_to_chromadb()

        # Build filter if category specified
        where = None
        if category_filter:
            where = {"category": category_filter}

        # Query ChromaDB
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        # Extract documents and metadata
        docs = results["documents"][0] if results["documents"] else []
        metas = results["metadatas"][0] if results["metadatas"] else []

        retrieved = []
        for doc, meta in zip(docs, metas):
            retrieved.append({
                "text": doc,
                "category": meta.get("category", "general")
            })

        return retrieved

    except Exception as e:
        print(f"Retrieval error: {e}")
        return []


def format_context_for_prompt(retrieved_docs):
    """Format retrieved docs into a clean context string for AI"""
    if not retrieved_docs:
        return "No specific knowledge found."

    context_parts = []
    for i, doc in enumerate(retrieved_docs, 1):
        category = doc["category"].replace("_", " ").title()
        context_parts.append(f"[{i}] ({category}): {doc['text']}")

    return "\n\n".join(context_parts)