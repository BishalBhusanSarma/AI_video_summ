import nltk
nltk.download('punkt')
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import CouldNotRetrieveTranscript
from langdetect import detect
from deep_translator import GoogleTranslator
import re

from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        elif parsed.path.startswith("/v/"):
            return parsed.path.split("/")[2]

    elif parsed.hostname == "youtu.be":
        return parsed.path[1:]

    raise ValueError("Invalid YouTube URL format")

import time

def translate_to_english(text, chunk_size=5000):
    translator = GoogleTranslator(source='auto', target='en')
    translated = []

    print("🔍 Detected language, translating to English...")

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        if not chunk.strip():
            continue  # Skip empty chunks

        if len(chunk.encode("utf-8")) > 4800:
            chunk = chunk.encode("utf-8")[:4800].decode("utf-8", "ignore")

        for attempt in range(3):
            try:
                print(f"Translating chunk ({i}-{i+chunk_size}) length: {len(chunk)}")
                translated_chunk = translator.translate(chunk)
                translated.append(translated_chunk)
                break  # success
            except Exception as e:
                print(f"⚠️ Retry {attempt+1} failed: {e}")
                time.sleep(2)
        else:
            print("❌ All retries failed, keeping original text.")
            translated.append(chunk)  # fallback: keep original

    return " ".join(translated)

import os

def get_transcript(url):
    """
    Retrieve the transcript of a YouTube video, optionally using a proxy.
    # Set proxy manually or via .env as YOUTUBE_PROXY (e.g., http://127.0.0.1:8080)
    Set the environment variable YOUTUBE_PROXY to use a proxy (e.g. http://127.0.0.1:8080).
    """
    video_id = get_video_id(url)

    proxy = os.getenv("YOUTUBE_PROXY")  # optional: set this in .env or system environment
    # Example: export YOUTUBE_PROXY="http://127.0.0.1:8080"
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    try:
        # Try to get an English transcript first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], proxies=proxies)
    except NoTranscriptFound:
        # Fallback: Get all available transcripts and pick the first one (even if not English)
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_obj = transcripts.find_transcript([t.language_code for t in transcripts])
            transcript = transcript_obj.fetch(proxies=proxies)
        except Exception as e:
            raise RuntimeError(f"❌ No usable transcripts found: {e}")
    except Exception as e:
        print(f"⚠️ Proxy request failed: {e}, retrying without proxy...")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except Exception as e2:
            raise RuntimeError(f"❌ Error retrieving transcript: {e2}")

    text = " ".join([x.text if hasattr(x, "text") else x['text'] for x in transcript])
    try:
        lang = detect(text)
    except:
        print("⚠️ Language detection failed, assuming non-English.")
        lang = "unknown"
    if lang != 'en':
        text = translate_to_english(text)

    return text