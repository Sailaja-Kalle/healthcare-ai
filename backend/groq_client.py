import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    """Initialize and return Groq client"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)

def get_ai_response(prompt, model="llama-3.3-70b-versatile", max_tokens=1000):
    """Get response from Groq AI"""
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI healthcare assistant for India. Always be caring, simple and helpful."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI service error: {str(e)}"

def get_streaming_response(prompt, model="llama-3.3-70b-versatile"):
    """Get streaming response from Groq AI"""
    try:
        client = get_groq_client()
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI healthcare assistant for India."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.7,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error: {str(e)}"