#
# Uncomment this if you have Ollama running locally and want to use a local LLM instead of Groq
# import subprocess
#
# def run_llama3_local(prompt):
#     result = subprocess.run(
#         ["ollama", "run", "llama3", prompt],
#         capture_output=True,
#         text=True
#     )
#     return result.stdout.strip()
from openai import OpenAI
from openai import OpenAIError, RateLimitError, APIError, AuthenticationError

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

client = OpenAI(api_key=st.secrets["groq_api_key"], base_url="https://api.groq.com/openai/v1")

from text_chunker import prepare_transcript_chunks

import time

#
# Uncomment below to use local LLM via Ollama instead of Groq API
# def run_groq_llama3(prompt, retries=5, delay=6):
#     return run_llama3_local(prompt)

def run_groq_llama3(prompt, retries=5, delay=6):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            print(f"Rate limit reached. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
    raise Exception("Exceeded maximum retry attempts due to rate limiting.")

# Uncomment this to use Ollama locally instead of Groq
# def run_groq_llama3(prompt, retries=5, delay=6):
#     return run_llama3_local(prompt)

def refine_summary(summaries):
    combined = "\n\n".join(summaries)
    prompt = f"""
        Given the following partial summaries from different parts of a YouTube transcript, merge and refine them into a final detailed and clean study note for the user.

        Make sure there are no duplicates, and the flow is logical and readable.

        Summaries:
        \"\"\"
        {combined}
        \"\"\"
    """
    return run_groq_llama3(prompt)

def generate_summary(text):
    chunks = prepare_transcript_chunks(text, 2000)
    summaries = []

    for chunk in chunks:
        prompt = f"""
            You are a highly knowledgeable teaching assistant trained on advanced computer science and technical subjects. Your job is to extract deep insights from a YouTube video transcript chunk and present a clear, rich, and highly structured summary that helps students deeply understand the material.

            Analyze the transcript below and output a detailed and logically ordered study note covering:

            - 🔍 A concise overview of the main topic covered
            - 📘 Key concepts and definitions, with simple explanations
            - 🔄 Step-by-step breakdowns of any processes, algorithms, or flows described
            - 🧠 Any examples or analogies used by the speaker
            - 🛠️ Practical applications, real-world usage, or programming contexts
            - ❗ Common misconceptions or tricky concepts (with clarifications)
            - ❓ Any implicit questions being answered or implied student doubts

            Be thorough, avoid repetition, and assume your summary will be used for revision or as a part of a course material. Use bullet points where appropriate and maintain clear sectioning.

            Transcript:
            \"\"\"
            {chunk}
            \"\"\"
        """
        summary = run_groq_llama3(prompt)
        summaries.append(summary)

    return refine_summary(summaries)