Title: AI-Powered YouTube Video Summarization and Concept Linking Using Local LLMs

Abstract:
This paper presents a lightweight, client-side system that automatically transcribes, translates, and summarizes educational YouTube videos using locally hosted Large Language Models (LLMs), specifically LLaMA 3.2. Additionally, it extracts concept-specific queries and generates relevant Google search links for further learning. The system is implemented using Python and Streamlit, designed to be privacy-preserving, cost-efficient, and extensible.

1. Introduction

Online educational content is growing rapidly, yet extracting key insights from lengthy YouTube lectures or tutorials remains a time-consuming task. This project introduces an application that automates this process using open-source tools, including:

YouTube transcript extraction

Language detection and translation

Chunked summarization with LLaMA 3.2 via Ollama

Smart keyword-based search suggestion

The entire pipeline runs locally on a Mac M1 with 8GB RAM, optimizing both memory and token limits through quantization and chunking.

2. System Architecture

2.1 Transcript Extraction
The system uses the youtube-transcript-api library to fetch captions from a YouTube video. If English captions are unavailable, it retrieves and uses the most accessible language transcript.

2.2 Translation and Preprocessing
Using langdetect and deep_translator, the transcript is detected for its language. If not English, it is chunked and translated (up to 4800 UTF-8 bytes) using retry-safe logic.

2.3 Summarization
The translated transcript is split into logical chunks (4500-6000 tokens), passed to LLaMA 3.2 (quantized with q4_K_M) via Ollama. Each chunk is summarized with an instructional prompt, and all summaries are merged using a refining step.

2.4 UI and Feedback Loop
Streamlit serves as the frontend. A loading animation cycles through motivational status messages during processing. Once the summarization is complete, the app displays the notes and suggested Google search links generated from structured question prompts.

3. Key Modules

app.py: Orchestrates Streamlit interface and the summarization workflow.

transcript_utils.py: Handles video ID parsing, transcript extraction, and language-aware translation.

text_chunker.py: Prepares chunks for LLM by handling translation, token limits, and encoding.

summarizer.py: Manages prompt engineering, chunk-level summarization, and final synthesis.

concept_links.py: Extracts dominant topics and converts them into Google search queries.

4. Optimizations for M1 Mac (8GB)

Uses quantized LLaMA models (q4_K_M) via Ollama to reduce memory pressure.

Caps chunk token size at 4500-6000 to stay within local LLM limits.

Avoids multithreading for UI updates to prevent NoSessionContext errors.

Translation retries and chunk slicing handle API instability.

5. Applications and Impact

Exam Preparation: Students can ingest entire lecture videos into structured notes.

Language Inclusion: Works well for non-English content (e.g., Hindi-English mix).

Offline Privacy: All processing occurs locally, with no cloud dependency.

6. Future Enhancements

Add MCQ generator and flashcard export.

Integrate local translation models to remove API reliance.

Enable topic-wise summaries and chapter separation.

Conclusion
This system demonstrates how local LLMs and open tools can provide powerful educational summarization and search augmentation in a privacy-preserving manner. It is efficient enough to run on everyday hardware and is extensible for various educational use-cases.