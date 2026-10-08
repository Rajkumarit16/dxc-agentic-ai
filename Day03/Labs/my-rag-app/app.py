import hashlib
import json
import sys
from datetime import date
from io import BytesIO
from pathlib import Path

import numpy as np
import streamlit as st
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from askit_core import bedrock, config

EMBED_MODEL = "amazon.titan-embed-text-v2:0"
st.set_page_config(page_title="AskMyPDF", page_icon="🦉")

# Give the app a teal-and-coral identity without changing the shared repo theme.
st.markdown("""
<style>
h1 { color: #087f78; }
.stChatMessage { border-radius: 12px; border: 1px solid #d8e8e5; }
.stButton > button { background: #087f78; color: white; border: 0; }
.stButton > button:hover { background: #c45b42; color: white; }
.about-card { padding: 12px; border-left: 4px solid #c45b42; background: #f1f7f5; }
</style>
""", unsafe_allow_html=True)


def embed(client, text):
    """Turn text into a Titan vector so meaning can be compared."""
    body = json.dumps({"inputText": text, "dimensions": 512, "normalize": True})
    result = client.invoke_model(modelId=EMBED_MODEL, body=body)
    return json.loads(result["body"].read())["embedding"]


def cosine(left, right):
    """Measure how closely two text vectors point in the same direction."""
    left, right = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    return float(np.dot(left, right) / denominator) if denominator else 0.0


def make_chunks(pdf_bytes, size, overlap):
    """Extract page-aware word chunks so every source can be cited."""
    reader = PdfReader(BytesIO(pdf_bytes))
    chunks = []
    step = size - overlap
    for page_number, page in enumerate(reader.pages, 1):
        words = (page.extract_text() or "").split()
        for start in range(0, len(words), step):
            text = " ".join(words[start:start + size])
            if text:
                chunks.append({"page": page_number, "text": text})
    return len(reader.pages), chunks


# Keep the uploaded PDF's index and chat across Streamlit reruns.
for key, value in {"pdf_hash": None, "chunks": [], "vectors": [], "messages": [],
                   "indexed_settings": None, "queued_question": None}.items():
    st.session_state.setdefault(key, value)

st.title("🦉 AskMyPDF")
st.caption("Upload. Ask. Done.  |  A calm, friendly guide to your own documents.")
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top-K sources", 1, 6, 3)
    chunk_size = st.slider("Chunk size (words)", 30, 300, 120)
    overlap = st.slider("Chunk overlap (words)", 0, min(100, chunk_size - 1), min(30, chunk_size - 1))
    if st.button("Clear chat", icon=":material/delete_sweep:"):
        st.session_state.messages = []
    st.markdown(
        f'<div class="about-card"><b>About me</b><br>AskIT learner<br>{date.today():%B %d, %Y}'
        '<br>Fun line: Curiosity is the best search query.</div>',
        unsafe_allow_html=True,
    )

uploaded = st.file_uploader("Choose a text-based PDF", type="pdf")
pdf_bytes = uploaded.getvalue() if uploaded else None
current_hash = hashlib.sha256(pdf_bytes).hexdigest() if pdf_bytes else None

# A new or removed PDF must never leave old sources or answers in the chat.
if current_hash != st.session_state.pdf_hash:
    st.session_state.pdf_hash = current_hash
    st.session_state.chunks, st.session_state.vectors = [], []
    st.session_state.messages, st.session_state.indexed_settings = [], None

if uploaded and st.button("Build index", type="primary", icon=":material/search:"):
    try:
        page_count, chunks = make_chunks(pdf_bytes, chunk_size, overlap)
        if not chunks:
            st.warning("No text found in this PDF. Try a PDF where you can select and copy text.")
        else:
            progress = st.progress(0, text="Reading your PDF and building its index...")
            client = bedrock.client()
            vectors = []
            for batch_start in range(0, len(chunks), 4):
                for item in chunks[batch_start:batch_start + 4]:
                    vectors.append(embed(client, item["text"]))
                progress.progress(min(1.0, len(vectors) / len(chunks)))
            st.session_state.chunks, st.session_state.vectors = chunks, vectors
            st.session_state.indexed_settings = (chunk_size, overlap)
            st.success(f"Indexed {page_count} pages into {len(chunks)} chunks.")
    except Exception:
        st.error("I couldn't build the index. Check your .env keys, AWS region, and Titan model access, then try again.")

ready = bool(st.session_state.chunks) and st.session_state.indexed_settings == (chunk_size, overlap)
if st.session_state.chunks and not ready:
    st.info("Chunk settings changed. Click Build index to apply them before asking another question.")

# Render stored turns with their evidence so sources remain visible after reruns.
for message in st.session_state.messages:
    avatar = "🦉" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            st.caption(message["badge"])
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(f'**Page {source["page"]} · similarity {source["score"]:.2f}**')
                    st.write(source["text"])

if st.button("Not in my PDF?", disabled=not ready, icon=":material/help:"):
    st.session_state.queued_question = "What is the current weather in Tokyo?"
question = st.session_state.queued_question or st.chat_input(
    "Ask a question about your PDF", disabled=not ready
)
st.session_state.queued_question = None

if question and ready:
    st.session_state.messages.append({"role": "user", "content": question})
    try:
        query_vector = embed(bedrock.client(), question)
        ranked = sorted(
            ((cosine(query_vector, vector), index) for index, vector in enumerate(st.session_state.vectors)),
            reverse=True,
        )[:top_k]
        sources = [{**st.session_state.chunks[index], "score": score} for score, index in ranked]
        context = "\n".join(f'[p.{item["page"]}] {item["text"]}' for item in sources)
        prompt = (
            "You are a calm, friendly guide. Be concise and use plain English. "
            "Answer ONLY from the context below. If the answer is not in it, say you could not find it in the PDF. "
            "Cite supporting pages like [p.3].\n\n"
            f"Context:\n{context}\n\nQuestion: {question}"
        )
        response = bedrock.client().converse(
            modelId=config.SMALL_MODEL,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 500, "temperature": 0.2},
        )
        answer = response["output"]["message"]["content"][0]["text"]
        badge = "grounded" if sources[0]["score"] >= 0.35 else "weak match"
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources, "badge": badge}
        )
        st.rerun()
    except Exception:
        st.error("I couldn't reach AWS. Check your .env keys, AWS region, and Titan/Nova model access, then retry.")

if st.session_state.messages:
    transcript = "\n\n".join(
        f'**{item["role"].title()}:** {item["content"]}' for item in st.session_state.messages
    )
    st.download_button("Download chat as Markdown", transcript, file_name="askmypdf-chat.md")

st.caption("Built by AskIT learner with vibe coding at DevPro Academy")