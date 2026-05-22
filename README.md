# 🏥 AI Healthcare Assistant

A production-level AI-powered Healthcare Assistant built with Python, Streamlit, Groq AI, and RAG technology — designed for Indian users.

## 🌐 Live Demo
👉 [Streamlit App](https://healthcare-ai-india.streamlit.app)
👉 [Render App](https://healthcare-ai-psbr.onrender.com)

## ✨ Features

- 🔍 **Hospital Finder** — Find nearby hospitals by city and symptoms
- 💬 **AI Chat** — Chat with AI healthcare assistant
- 💰 **Cost Estimator** — Get treatment cost estimates (Government vs Private)
- 📚 **Medical Knowledge Base** — RAG-powered medical Q&A with ChromaDB
- 📜 **Chat History** — Save and view your search history
- 🎤 **Voice Input** — Speak your symptoms
- 🔊 **Voice Output** — Listen to AI responses
- 🌍 **Multilingual** — English, Telugu, Hindi
- 🗺️ **Hospital Maps** — View hospitals on interactive map
- 🔐 **User Login** — Register, login, guest mode
- 🚨 **Emergency Detection** — Auto-detect emergencies, show 108 alert
- 🤖 **Symptom Checker** — Step-by-step AI diagnosis agent

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core language |
| Streamlit | Web UI framework |
| Groq AI (LLaMA 3.3 70B) | AI responses |
| ChromaDB | Vector database for RAG |
| Sentence Transformers | Text embeddings |
| SQLite + bcrypt | User auth & history |
| gTTS | Text to speech |
| Folium | Interactive maps |
| Pandas | Data processing |

## 📁 Project Structure

healthcare-ai/
├── app.py                  # Main entry point
├── ui.py                   # Main UI with all tabs
├── backend/
│   ├── groq_client.py      # Groq AI integration
│   ├── recommendation_engine.py
│   ├── emergency_detector.py
│   └── cost_estimator.py
├── frontend/
│   ├── chatbot_ui.py
│   ├── login_ui.py
│   ├── history_ui.py
│   ├── hospital_cards.py
│   ├── map_view.py
│   └── sidebar.py
├── rag/
│   ├── medical_knowledge.py
│   ├── chroma_manager.py
│   ├── document_loader.py
│   ├── retriever.py
│   └── embeddings.py
├── database/
│   ├── models.py
│   ├── auth.py
│   └── history.py
├── voice/
│   └── speech_to_text.py
├── utils/
│   └── prompts.py
└── requirements.txt

## 🚀 Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/Sailaja-Kalle/healthcare-ai.git
cd healthcare-ai
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file:**


GROQ_API_KEY=your_groq_api_key_here

**4. Run the app:**
```bash
streamlit run app.py
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Get free key from [groq.com](https://groq.com) |

## 👩‍💻 Built By

**Sailaja Kalle**
- GitHub: [@Sailaja-Kalle](https://github.com/Sailaja-Kalle)

