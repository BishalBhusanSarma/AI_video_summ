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

youtube_url = st.text_input("Paste YouTube Video URL:")

if youtube_url:
    with st.spinner("🔄 Fetching transcript and preparing chunks..."):
        transcript = get_transcript(youtube_url)
        st.subheader("🗒️ Transcript with Timestamps")
        for entry in transcript:
            if isinstance(entry, dict) and 'start' in entry and 'text' in entry:
                start_time = time.strftime('%H:%M:%S', time.gmtime(entry['start']))
                st.markdown(f"**[{start_time}]** {entry['text']}")
        chunks = prepare_transcript_chunks(transcript)

        messages = [
            "🔄 Preparing your personalized notes",
            "⏳ Gathering key insights from the video",
            "✨ We are almost ready"
        ]

        all_summaries = []
        placeholder = st.empty()
        message_cycle = itertools.cycle(messages)

        for i, chunk in enumerate(chunks):
            message = next(message_cycle)
            dots = "." * ((i % 3) + 1)
            placeholder.markdown(f"{message}{dots}")
            summary = generate_summary(chunk)
            all_summaries.append(summary)
            time.sleep(4)

        placeholder.empty()

    final_summary = "\n\n".join(all_summaries)
    st.subheader("📝 Final Summary Notes")
    st.write(final_summary)

    st.subheader("🔍 Explore Related Topics")
    search_links = generate_google_search_links(final_summary)
    for question, url in search_links.items():
        st.markdown(f"- [{question}]({url})")