import os
import re
import string

import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()
PUNCTUATION_RE = re.compile(f"[{re.escape(string.punctuation)}]")


def clean_text(text):
    text = text.lower()
    text = PUNCTUATION_RE.sub(" ", text)
    tokens = word_tokenize(text)
    tokens = [
        LEMMATIZER.lemmatize(token)
        for token in tokens
        if token.isalpha() and token not in STOP_WORDS
    ]
    return " ".join(tokens)