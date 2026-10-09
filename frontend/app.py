
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide",
)

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background: #f8fafc;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}
[data-testid="stFileUploader"] {
    background: white;
    border: 1px dashed #60a5fa;
    border-radius: 14px;
    padding: 12px;
}
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 12px;
}
.section-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
}
.small-muted {
    color: #64748b;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None

# ---------- Header ----------
st.title("📚 DocuMind AI")
st.caption(
    "Chat with your documents using Retrieval-Augmented Generation (RAG)."
)

st.divider()

# ---------- Two-column layout ----------
left_col, right_col = st.columns([1, 2.2], gap="large")

# ======================================
# LEFT: Document Upload
# ======================================
with left_col:
    st.subheader("📂 Your Documents")
    st.markdown(
        '<div class="small-muted">'
        'Upload a PDF to start asking questions.'
        '</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Drag and drop your PDF here",
        type=["pdf"],
        help="PDF files only",
    )

    if uploaded_file is not None:
        st.caption(f"Selected: {uploaded_file.name}")

        if st.button(
            "⬆️ Upload Document",
            use_container_width=True,
            type="primary",
        ):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }

            try:
                with st.spinner("Processing document..."):
                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=180,
                    )

                if response.ok:
                    st.session_state.uploaded_name = (
                        uploaded_file.name
                    )
                    st.success("Document uploaded successfully!")
                    st.caption(
                        "You can now ask questions about this document."
                    )
                else:
                    st.error(
                        f"Upload failed ({response.status_code}): "
                        f"{response.text[:300]}"
                    )

            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to the API: {exc}")

    st.divider()
    st.markdown("**📄 Current document**")

    if st.session_state.uploaded_name:
        st.success(st.session_state.uploaded_name)
    else:
        st.info("No document uploaded yet.")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ======================================
# RIGHT: Chat Assistant
# ======================================
with right_col:
    st.subheader("💬 AI Assistant")
    st.caption("Ask questions and explore your document.")

    chat_area = st.container()

    with chat_area:
        if not st.session_state.chat_history:
            st.info(
                "👋 Welcome! Upload a PDF on the left, "
                "then ask your first question below."
            )

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):
                st.write(chat["answer"])

                if chat.get("sources"):
                    with st.expander("📚 View sources"):
                        for i, source in enumerate(
                            chat["sources"], start=1
                        ):
                            st.markdown(f"**Source {i}**")
                            st.caption(
                                f"File: {source.get('source', 'Unknown')} "
                                f"| Page: {source.get('page', 'N/A')}"
                            )
                            st.write(source.get("content", ""))

    question = st.chat_input(
        "Ask something about your documents..."
    )

    if question:
        if not st.session_state.uploaded_name:
            st.warning("Please upload a document first.")
        else:
            history = [
                {
                    "question": item["question"],
                    "answer": item["answer"],
                }
                for item in st.session_state.chat_history
            ]

            try:
                with st.spinner("Searching your documents..."):
                    response = requests.post(
                        f"{API_URL}/ask",
                        json={
                            "question": question,
                            "chat_history": history,
                        },
                        timeout=120,
                    )

                if response.ok:
                    data = response.json()

                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": data["answer"],
                        "sources": data.get("sources", []),
                    })

                    st.rerun()
                else:
                    st.error(
                        f"Request failed ({response.status_code}): "
                        f"{response.text[:300]}"
                    )

            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to the API: {exc}")