# Electronics Store FAQ Chatbot

A local, rule-free FAQ chatbot for an electronics store. Users type questions in natural
language and the bot finds the most similar question in a pre-built FAQ knowledge base
using NLP preprocessing + TF-IDF vectorization + cosine similarity — no if-else matching
rules. It runs with a simple Streamlit web UI.

## Features

- Natural-language question matching with a configurable minimum score (default `0.35`)
- NLTK-based text preprocessing: lowercase → remove punctuation → tokenize → remove
  stopwords → lemmatize
- TF-IDF vectorizer fitted once on all FAQ questions at startup for fast lookups
- Special commands:
  - `hi` / `hello` / `hey` → greeting message
  - `bye` / `quit` / `exit` / `goodbye` → goodbye message
  - empty input → "Please type a question."
- Streamlit chat UI:
  - `st.chat_message` bubbles and full chat history in `st.session_state`
  - "Clear Chat" button
  - Clickable suggested questions (all 20 from the knowledge base) with
    "Load more questions" (+6 per click) and "Show less questions" options
  - Sidebar showing the FAQ count and a threshold slider (0.0–1.0)

## Project structure

| File                | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| `data/faqs.json`    | Knowledge base: 20 Q&A pairs (warranty, returns, delivery, EMI, installation, troubleshooting, support) |
| `preprocess.py`     | NLTK downloads + `clean_text()` preprocessing pipeline                   |
| `matcher.py`        | `FaqMatcher` — fits TF-IDF, computes cosine similarity, returns answers  |
| `app.py`            | Streamlit chat application (UI + session state)                          |
| `requirements.txt`  | Python dependencies                                                       |

## How it works

1. `preprocess.py` — `clean_text(text)` lowercases, strips punctuation, tokenizes,
   removes stopwords and non-alphabetic tokens, and lemmatizes (WordNetLemmatizer).
   On first import it downloads the NLTK resources: `punkt`, `punkt_tab`, `stopwords`,
   `wordnet`, `omw-1.4`.
2. `matcher.py` — `FaqMatcher` loads `data/faqs.json`, cleans all FAQ questions, and
   fits a `TfidfVectorizer` once at startup (`__init__`).
3. `get_response(user_text, threshold)` — commands are handled first, otherwise the
   user's question is cleaned, transformed, and cosine similarity is computed against
   the FAQ matrix. If the best score `>= threshold` (default `0.35`) the FAQ answer is
   returned; otherwise:

   > Sorry, I don't have an answer for that. Please rephrase or contact support.

## Requirements

- Python 3.9+
- Packages in `requirements.txt`: `streamlit`, `scikit-learn`, `nltk`

## Setup

```bash
cd "FAQ Chatbot — Question-Answering Assistant (task 2)"

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

The required NLTK data (`punkt`, `punkt_tab`, `stopwords`, `wordnet`, `omw-1.4`) is
downloaded automatically the first time `preprocess.py` is imported.

## Running the app

```bash
streamlit run app.py
```

or, if using the shared virtual environment in the workspace root:

```bash
/Applications/task/.venv/bin/streamlit run app.py
```

Open the URL Streamlit prints (by default <http://localhost:8501>).

## Usage

- Ask a question in the chat input box — e.g. "How long does delivery take?"
- Click any suggested question to send it instantly; use "Load more questions" /
  "Show less questions" to browse the full list of 20.
- Use the sidebar to see the FAQ count, adjust the match threshold, or click
  "Clear Chat" to reset the conversation.
- Try `hi`/`hello` for a greeting and `bye`/`quit` for a goodbye message.

## Configurable parameters

| Constant                    | Location    | Default                                   |
| --------------------------- | ----------- | ----------------------------------------- |
| `DEFAULT_THRESHOLD`         | `matcher.py` | `0.35` (minimum cosine similarity score) |
| `FALLBACK_MESSAGE`          | `matcher.py` | "Sorry, I don't have an answer..."       |
| `GREETING_MESSAGE` / `GOODBYE_MESSAGE` / `EMPTY_MESSAGE` | `matcher.py` | greeting / goodbye / "Please type a question." |
| `QUESTIONS_PER_PAGE`        | `app.py`    | `6` (questions shown per load batch)      |

The threshold can also be changed live in the UI via the sidebar slider without
restarting the app.