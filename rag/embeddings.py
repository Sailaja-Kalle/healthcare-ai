# Disabled for deployment

def get_rag_response(query, language="English", n_results=4):
    return query, []

def stream_rag_response(query, language="English"):
    yield "", "", []