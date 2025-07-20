# 🎥 YouTube Notes App (AI-Powered Summarizer)

Paste a YouTube link. Get:
- ✅ Bullet-point summary
- 🌐 Auto-translation to English (if needed)
- 🔎 Google links for further research
- 💬 Ask up to 15 follow-up questions via chat

---

## ⚙️ Features

- 📺 **YouTube Transcription**: Extract subtitles/transcripts (even translated)
- 🧠 **LLM-Powered Summarization**: Local (Ollama) or API-based (Groq)
- 🌍 **Multilingual Support**: Auto-detects and translates to English
- 💬 **Chat Interface**: Ask questions about the video content (15-question limit)
- 🔒 **Runs locally or deploys on Streamlit Cloud**

---

## 🧪 Tech Stack

- [Streamlit](https://streamlit.io/) — Web UI
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [Langchain](https://github.com/langchain-ai/langchain)
- [Groq API](https://console.groq.com/)
- [Ollama](https://ollama.com/) (for local LLaMA3)
- [Deep Translator](https://pypi.org/project/deep-translator/) (for auto translation)

---

## 🚀 Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Start local LLM (only if using Ollama)
ollama run llama3

# 5. Run the Streamlit app
streamlit run app.py