from fastapi import FastAPI , File, HTTPException , UploadFile
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.embeddings import create_embeddings
from backend.app.vectorstore import add_documents, collection
from pydantic import BaseModel
from backend.app.rag_chain import ask_question
from typing import List
import logging

UPLOAD_DIR = Path("data")
UPLOAD_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Document RAG API",
    description="RAG API for question answering over documents",
    version="1.0.0"
)


class ChatMessage(BaseModel):
    question: str
    answer: str


class QuestionRequest(BaseModel):
    question: str
    chat_history: List[ChatMessage] = []

@app.get("/")
async def home():
    return {"messages" : "Document RAG API is running"} 

    
@app.post("/upload")
async def split_document(file: UploadFile = File(...)):
    
    logger.info(f"Upload started: {file.filename}")
    # 1. Save the uploaded PDF
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. Load the PDF
    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    # 3. Create the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    # 4. Split the document into chunks
    chunks = text_splitter.split_documents(documents)
    
    embeddings = create_embeddings(chunks)
    
    number_of_chunks = add_documents(
        chunks,
        embeddings
    )
    
    logger.info(
        f"Document processed: {file.filename} | "
        f"Chunks: {len(chunks)}"
    )


    # 5. Return information about the chunks
    return {
        "filename": file.filename,
        "pages": len(documents),
        "total_chunks": len(chunks),
        "first_chunk": chunks[0].page_content if chunks else "",
        "first_chunk_metadata": chunks[0].metadata if chunks else {},
        "chunks": len(chunks),
        "embeddings_shape": embeddings.shape,
        "ChromaDB count:": collection.count()
    }
    
    
@app.post("/ask")
def ask(request: QuestionRequest):

    logger.info(f"Question received: {request.question}")

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        history = [
            {
                "question": message.question,
                "answer": message.answer
            }
            for message in request.chat_history
        ]

        result = ask_question(
            request.question,
            history
        )
        
        logger.info(
            f"Retrieved {len(result['sources'])} sources"
        )

        sources = []

        for document in result["sources"]:
            sources.append({
                "page": document.metadata.get("page"),
                "source": document.metadata.get("source"),
                "content": document.page_content
            })

        return {
            "answer": result["answer"],
            "sources": sources
        }

    except RuntimeError as e:

        logger.error(f"RAG error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )