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

def get_transcript(url):
    video_id = get_video_id(url)

    try:
        # Try to get an English transcript first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        # Fallback: Get all available transcripts and pick the first one (even if not English)
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_obj = transcripts.find_transcript([t.language_code for t in transcripts])
            transcript = transcript_obj.fetch()
        except Exception as e:
            raise RuntimeError(f"❌ No usable transcripts found: {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Error retrieving transcript: {e}")

    text = " ".join([x.text if hasattr(x, "text") else x['text'] for x in transcript])
    lang = detect(text)
    if lang != 'en':
        text = translate_to_english(text)

    return text