import time
import itertools
import streamlit as st
from transcript_utils import get_transcript
from summarizer import generate_summary
from concept_links import generate_google_search_links
from text_chunker import prepare_transcript_chunks

from openai import RateLimitError, AuthenticationError, APIError
st.set_page_config(page_title="AI YouTube Notes App", layout="wide")
st.title("🎬 YouTube Video AI Notes + Learning Resources")

# --- Session State Initialization ---
if 'transcript_data' not in st.session_state:
    st.session_state.transcript_data = None
if 'final_summary' not in st.session_state:
    st.session_state.final_summary = None
if 'chunks' not in st.session_state:
    st.session_state.chunks = None

# --- YouTube URL Input with Submit Button ---
with st.form("youtube_form"):
    youtube_url = st.text_input("Paste YouTube Video URL:")
    submit_url = st.form_submit_button("Process Video")

# --- Process YouTube Video Only On Submit ---
if submit_url and youtube_url:
    with st.spinner("🔄 Fetching transcript and preparing chunks..."):
        transcript = get_transcript(youtube_url)
        st.session_state.transcript_data = transcript
        st.session_state.chunks = prepare_transcript_chunks(transcript)

        all_summaries = []
        status_placeholder = st.empty()
        for i, chunk in enumerate(st.session_state.chunks):
            rotating_messages = [
                "🔄 Preparing your personalized notes...",
                "⏳ Gathering key insights from the video...",
                "✨ We are almost ready..."
            ]
            current_message = rotating_messages[i % len(rotating_messages)]
            status_placeholder.markdown(current_message)
            summary = generate_summary(chunk)
            all_summaries.append(summary)
            time.sleep(3)
        status_placeholder.empty()
        st.session_state.final_summary = "\n\n".join(all_summaries)

# --- Show Transcript and Summary if Available ---
if st.session_state.transcript_data:
    st.subheader("🗒️ Transcript with Timestamps")
    for entry in st.session_state.transcript_data:
        if isinstance(entry, dict) and 'start' in entry and 'text' in entry:
            start_time = time.strftime('%H:%M:%S', time.gmtime(entry['start']))
            st.markdown(f"**[{start_time}]** {entry['text']}")

if st.session_state.final_summary:
    st.subheader("📝 Final Summary Notes")
    st.write(st.session_state.final_summary)

    st.subheader("🔍 Explore Related Topics")
    search_links = generate_google_search_links(st.session_state.final_summary)
    for question, url in search_links.items():
        st.markdown(f"- [{question}]({url})")

# --- Question/Answer Section (Groq-like placeholder) ---
st.subheader("💬 Ask Questions about the Video")

if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

if st.session_state.question_count < 15:
    user_query = st.text_input("Enter your question here:")
    if st.button("Submit Question"):
        if user_query.strip():
            st.session_state.question_count += 1
            import requests
            import os

            # Example Groq API endpoint and key
            GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
            groq_api_key = st.secrets["groq_api_key"] if "groq_api_key" in st.secrets else os.getenv("groq_api_key")

            try:
                response = requests.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-70b-8192",
                        "messages": [
                            {"role": "system", "content": "You are a helpful mate who wxplains the topic in very simple and easy to understand language."},
                            {"role": "user", "content": user_query}
                        ],
                        "temperature": 0.7
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    st.markdown(f"**Answer:** {answer}")
                else:
                    st.error(f"Groq API error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to fetch Groq API response: {e}")
else:
    st.warning("❗ You have reached the 15-question limit.")