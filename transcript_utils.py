import nltk

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
import random
def get_webshare_proxies():
    proxy_list = [
        "http://ckugxxjz:ialikg3g0dry@38.154.227.167:5868",
        "http://ckugxxjz:ialikg3g0dry@23.95.150.145:6114",
        "http://ckugxxjz:ialikg3g0dry@198.23.239.134:6540",
        "http://ckugxxjz:ialikg3g0dry@45.38.107.97:6014",
        "http://ckugxxjz:ialikg3g0dry@207.244.217.165:6712",
        "http://ckugxxjz:ialikg3g0dry@107.172.163.27:6543",
        "http://ckugxxjz:ialikg3g0dry@216.10.27.159:6837",
        "http://ckugxxjz:ialikg3g0dry@136.0.207.84:6661",
        "http://ckugxxjz:ialikg3g0dry@142.147.128.93:6593",
        "http://ckugxxjz:ialikg3g0dry@206.41.172.74:6634"
    ]
    return proxy_list

def get_transcript(url):
    """
    Retrieve the transcript of a YouTube video using rotating Webshare proxies.
    """
    video_id = get_video_id(url)

    proxies = None
    proxies_list = get_webshare_proxies()
    random.shuffle(proxies_list)

    for proxy_url in proxies_list:
        proxies = {'http': proxy_url, 'https': proxy_url}
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], proxies=proxies)
            break
        except NoTranscriptFound:
            try:
                transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript_obj = transcripts.find_transcript([t.language_code for t in transcripts])
                transcript = transcript_obj.fetch(proxies=proxies)
                break
            except Exception as e:
                print(f"⚠️ Proxy {proxy_url} failed during fallback: {e}")
        except Exception as e:
            print(f"⚠️ Proxy {proxy_url} failed: {e}")
    else:
        raise RuntimeError("❌ All proxies failed or no transcript available.")

    text = " ".join([x.text if hasattr(x, "text") else x['text'] for x in transcript])
    try:
        lang = detect(text)
    except:
        print("⚠️ Language detection failed, assuming non-English.")
        lang = "unknown"
    if lang != 'en':
        text = translate_to_english(text)

    return text