from rag.retriever import retrieve_relevant_docs, format_context_for_prompt
from backend.groq_client import get_streaming_response

def get_rag_response(query, language="English", n_results=4):
    """Full RAG pipeline: retrieve + generate"""

    # Step 1: Retrieve relevant docs
    retrieved_docs = retrieve_relevant_docs(query, n_results=n_results)

    # Step 2: Format context
    context = format_context_for_prompt(retrieved_docs)

    # Step 3: Language instruction
    lang_instructions = {
        "English": "Reply in English only.",
        "Telugu": "మీరు తప్పనిసరిగా తెలుగులో మాత్రమే సమాధానం ఇవ్వాలి. Do not use English at all.",
        "Hindi": "आपको केवल हिंदी में जवाब देना है। अंग्रेजी का बिल्कुल उपयोग न करें।"
    }
    lang_instruction = lang_instructions.get(language, lang_instructions["English"])

    # Step 4: Build RAG prompt
    prompt = f"""You are an expert AI healthcare assistant for India.
Use the following verified medical knowledge to answer the user's question accurately.

KNOWLEDGE BASE:
{context}

USER QUESTION: {query}

STRICT LANGUAGE RULE: {lang_instruction}

Instructions:
- Answer using the knowledge provided above
- Be clear, simple and helpful for common people
- Always recommend consulting a real doctor for serious issues
- Mention government schemes if relevant (Ayushman Bharat, Aarogyasri etc.)
- For emergencies say: call 108 immediately
- YOU MUST WRITE EVERYTHING IN {language.upper()} ONLY
"""

    return prompt, retrieved_docs


def stream_rag_response(query, language="English"):
    """Stream RAG response chunk by chunk"""
    prompt, retrieved_docs = get_rag_response(query, language)

    full_response = ""
    for chunk in get_streaming_response(prompt):
        full_response += chunk
        yield chunk, full_response, retrieved_docs