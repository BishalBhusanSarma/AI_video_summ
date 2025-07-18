from deep_translator import GoogleTranslator
from langdetect import detect
import tiktoken

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text

def count_tokens(text, model_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

def split_text_into_chunks(text, max_tokens=6000, model_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i : i + max_tokens]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

def prepare_transcript_chunks(raw_text, max_tokens=6000):
    lang = detect(raw_text)
    if lang != 'en':
        raw_text = translate_to_english(raw_text)

    return split_text_into_chunks(raw_text, max_tokens=max_tokens)