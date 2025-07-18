# YouTube Notes App (LLM + Streamlit)

Paste a YouTube link. Get:
- Bullet-point summary
- Auto translation (if needed)
- Google links for research

### 🧠 Powered by:
- LLaMA 3.2 (via Ollama)
- LangChain
- Streamlit

### 📦 How to Run
```bash
git clone your-repo
cd youtube_notes_app
pip install -r requirements.txt
ollama run llama3
streamlit run app.py