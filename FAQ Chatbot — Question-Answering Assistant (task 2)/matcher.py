import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAQS_PATH = os.path.join(BASE_DIR, "data", "faqs.json")

DEFAULT_THRESHOLD = 0.35
FALLBACK_MESSAGE = "Sorry, I don't have an answer for that. Please rephrase or contact support."
GREETING_MESSAGE = "Hello! I'm your electronics store assistant. Ask me about warranties, returns, delivery, EMI, installation, or troubleshooting."
GOODBYE_MESSAGE = "Thanks for chatting! Have a great day. Feel free to come back anytime."
EMPTY_MESSAGE = "Please type a question."

GREETING_WORDS = {"hi", "hello", "hey", "hii", "hiii"}
GOODBYE_WORDS = {"bye", "quit", "exit", "goodbye", "see you", "see ya"}


class FaqMatcher:
    def __init__(self, faqs_path=FAQS_PATH):
        self.vectorizer = TfidfVectorizer()
        with open(faqs_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)
        self.questions = [item["question"] for item in self.faqs]
        cleaned_questions = [clean_text(q) for q in self.questions]
        self.tfidf_matrix = self.vectorizer.fit_transform(cleaned_questions)

    def get_response(self, user_text, threshold=DEFAULT_THRESHOLD):
        text = " ".join(user_text.strip().split())
        if not text:
            return EMPTY_MESSAGE

        normalized = text.lower()
        if normalized in GREETING_WORDS:
            return GREETING_MESSAGE
        if (
            normalized in GOODBYE_WORDS
            or normalized.startswith(tuple(GOODBYE_WORDS))
        ):
            return GOODBYE_MESSAGE

        if not self.tfidf_matrix.nnz:
            return FALLBACK_MESSAGE

        cleaned_query = clean_text(text)
        query_vector = self.vectorizer.transform([cleaned_query])
        scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        best_index = int(scores.argmax())
        best_score = float(scores[best_index])

        if best_score >= threshold:
            return self.faqs[best_index]["answer"]
        return FALLBACK_MESSAGE