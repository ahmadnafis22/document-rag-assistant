
import chromadb
from uuid import uuid4

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(chunks, embeddings):

    documents = [
        chunk.page_content
        for chunk in chunks
    ]

    metadatas = [
        chunk.metadata
        for chunk in chunks
    ]

    ids = [
        str(uuid4())
        for _ in chunks
    ]

    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    return len(chunks)