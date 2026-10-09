# DocuMind AI — Document RAG Assistant

An AI-powered document question-answering system that allows users to upload PDF files and ask questions about their content.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant document chunks and generate answers using Google Gemini.

## Features

* Upload PDF documents.
* Extract and split document text into chunks.
* Generate text embeddings using Sentence Transformers.
* Store and retrieve document chunks using ChromaDB.
* Answer questions using Google Gemini.
* Display document sources with answers.
* Maintain conversation history during a chat session.
* REST API built with FastAPI.
* Interactive frontend built with Streamlit.
* Automated tests using pytest.

## Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain
* Google Gemini
* Sentence Transformers
* Hugging Face
* ChromaDB
* Pytest

## Project Structure

```text
document-rag/
├── backend/
│   └── app/
│       ├── main.py
│       ├── embeddings.py
│       ├── vectorstore.py
│       ├── retriever.py
│       ├── context.py
│       ├── prompt.py
│       ├── llm.py
│       ├── rag_chain.py
│       ├── test_ask.py
│       └── test_upload.py
├── frontend/
│   └── app.py
├── data/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

1. Upload a PDF document through the frontend.
2. Extract text from the PDF.
3. Split the text into smaller chunks.
4. Generate embeddings for the chunks.
5. Store the embeddings and document text in ChromaDB.
6. Retrieve relevant chunks when a user asks a question.
7. Build a context-aware prompt.
8. Generate an answer using Google Gemini.
9. Display the answer and its document sources.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd document-rag
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_google_api_key
```

Never commit your real API key to GitHub.

### 5. Run the backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### 6. Run the frontend

Open a second terminal in the project root, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

## Running Tests

Run the automated tests from the project root:

```bash
python -m pytest -v
```

## Security

* Store API keys in environment variables.
* Do not upload `.env` to GitHub.
* Avoid committing private or sensitive documents.

## Future Improvements

* Support additional document formats.
* Improve retrieval relevance and filtering.
* Add Docker support.
* Deploy the application to a cloud platform.

## Author

AI Engineering Portfolio Project
