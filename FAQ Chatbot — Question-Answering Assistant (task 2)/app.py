import streamlit as st

from matcher import DEFAULT_THRESHOLD, FaqMatcher

st.set_page_config(
    page_title="Electronics Store FAQ Assistant",
    page_icon="💬",
    layout="centered",
)

QUESTIONS_PER_PAGE = 6

if "messages" not in st.session_state:
    st.session_state.messages = []

if "faq_matcher" not in st.session_state:
    st.session_state.faq_matcher = FaqMatcher()

matcher = st.session_state.faq_matcher

SUGGESTED_QUESTIONS = [faq["question"] for faq in matcher.faqs]

if "visible_questions" not in st.session_state:
    st.session_state.visible_questions = min(QUESTIONS_PER_PAGE, len(SUGGESTED_QUESTIONS))

# ---------------------------------------------------------------------------
# Sidebar: FAQ count + threshold slider + Clear Chat
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("FAQ Assistant")
    st.metric(label="FAQ count", value=len(matcher.faqs))
    threshold = st.slider(
        "Match threshold",
        min_value=0.0,
        max_value=1.0,
        value=DEFAULT_THRESHOLD,
        step=0.05,
        help="Minimum cosine similarity score required to accept a match.",
    )
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Header + suggested questions
# ---------------------------------------------------------------------------

st.title("Electronics Store FAQ Assistant")
st.caption("Ask anything about warranties, returns, delivery, EMI, installation, or troubleshooting.")

st.markdown("**Suggested questions:**")
visible_count = st.session_state.visible_questions
visible_questions = SUGGESTED_QUESTIONS[:visible_count]

for index in range(0, len(visible_questions), 2):
    row_questions = visible_questions[index : index + 2]
    columns = st.columns(len(row_questions))
    for column, question in zip(columns, row_questions):
        with column:
            if st.button(
                question,
                key=f"suggested_{question}",
                use_container_width=True,
            ):
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": matcher.get_response(question, threshold),
                    }
                )

can_load_more = visible_count < len(SUGGESTED_QUESTIONS)
can_show_less = visible_count > QUESTIONS_PER_PAGE

if can_load_more and can_show_less:
    load_col, less_col = st.columns(2)
    with load_col:
        if st.button("Load more questions", key="load_more_questions", use_container_width=True):
            st.session_state.visible_questions = min(
                visible_count + QUESTIONS_PER_PAGE,
                len(SUGGESTED_QUESTIONS),
            )
            st.rerun()
    with less_col:
        if st.button("Show less questions", key="show_less_questions", use_container_width=True):
            st.session_state.visible_questions = QUESTIONS_PER_PAGE
            st.rerun()
elif can_load_more:
    if st.button("Load more questions", key="load_more_questions", use_container_width=True):
        st.session_state.visible_questions = min(
            visible_count + QUESTIONS_PER_PAGE,
            len(SUGGESTED_QUESTIONS),
        )
        st.rerun()
else:
    if st.button("Show less questions", key="show_less_questions", use_container_width=True):
        st.session_state.visible_questions = QUESTIONS_PER_PAGE
        st.rerun()

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------

prompt = st.chat_input("Type your question here...")

if prompt is not None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = matcher.get_response(prompt, threshold)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)