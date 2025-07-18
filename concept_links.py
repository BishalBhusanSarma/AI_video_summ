import re
from urllib.parse import quote_plus
from collections import Counter

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

def extract_main_topic(summary):
    sentences = nltk.sent_tokenize(summary)
    words = [w for s in sentences for w in nltk.word_tokenize(s.lower()) if w.isalpha()]
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if w not in stop_words]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([' '.join(filtered_words)])
    tfidf_scores = dict(zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]))
    
    if not tfidf_scores:
        return "programming concepts"

    top_keyword = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[0][0]
    return top_keyword

def generate_search_queries(summary):
    topic = extract_main_topic(summary).title()

    return [
        f"Beginner's guide to {topic}",
        f"Advanced concepts in {topic}",
        f"Applications of {topic} in real-world scenarios",
        f"Common misconceptions about {topic}",
        f"Best resources to learn {topic}"
    ]

def generate_google_search_links(summary):
    queries = generate_search_queries(summary)
    return {
        q: f"https://www.google.com/search?q={quote_plus(q)}"
        for q in queries
    }