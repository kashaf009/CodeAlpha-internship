# Code Alpha AI Internship

This repository contains the mini projects completed during the Code Alpha AI
Internship.

---

## Task 1 — Language Translator Pro



A desktop translation app built with Python's Tkinter GUI and the
`deep_translator` library (Google Translator).

**Key features:**

- Translate between 16 languages (English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Italian, Japanese, Korean, Chinese, French, German, Spanish, Arabic, Russian)
- Swap source/target languages with one click
- Live character counter with a 500-character limit
- Copy-to-clipboard button for the translated text
- Keyboard shortcuts: `Ctrl+Enter` to translate, `Ctrl+C` to copy
- Background threading so the UI never freezes during translation

**Run:**

```bash
python task1/translator.py
```

---

## Task 2 — FAQ Chatbot — Question-Answering Assistant


A local, rule-free FAQ chatbot for an electronics store. Users type questions in
natural language and the bot finds the most similar question from a pre-built
knowledge base using NLP + cosine similarity (no if-else rules).

**Key features:**

- NLTK preprocessing: lowercase → remove punctuation → tokenize → remove stopwords → lemmatize
- `TfidfVectorizer` fitted once on startup; cosine similarity per query (threshold `0.35`)
- Knowledge base of 20 Q&A pairs: warranty, returns, delivery, EMI, installation, troubleshooting, support
- Streamlit chat UI: `st.chat_message` bubbles, chat history, Clear Chat button
- Clickable suggested questions with **Load more / Show less** options
- Sidebar: FAQ count + match-threshold slider
- Special commands: `hi`/`hello` → greeting, `bye`/`quit` → goodbye, empty input → "Please type a question."

**Run:**

```bash
/Applications/task/.venv/bin/streamlit run "FAQ Chatbot — Question-Answering Assistant (task 2)/app.py"
```

See [`FAQ Chatbot — Question-Answering Assistant (task 2)/README.md`](FAQ%20Chatbot%20—%20Question-Answering%20Assistant%20(task%202)/README.md)
for the full project documentation.

---

## Setup & Dependencies

Both projects use a shared virtual environment at `.venv/`.

```bash
# Install Task 1 dependencies
pip install deep-translator pyperclip beautifulsoup4

# Install Task 2 dependencies
pip install -r "FAQ Chatbot — Question-Answering Assistant (task 2)/requirements.txt"
```

Task 2 also downloads its required NLTK resources automatically on first run
(`punkt`, `punkt_tab`, `stopwords`, `wordnet`, `omw-1.4`).