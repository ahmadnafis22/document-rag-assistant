from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="data/chroma_db"
)

#=================================#
# MMR
    # search_type="mmr",
    # search_kwargs={
    #     "k": 3,
    #     "fetch_k": 10,
    #     "lambda_mult": 0.5
    # }   
#=================================# 

retriever = vectorstore.as_retriever(
    
      search_type="similarity",
      search_kwargs={
         "k": 3
      }

)

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = model.encode(texts)

    return embeddings


def retrieve_relevant_documents(
    question: str,
    threshold: float = 1.3,
    k: int = 5
):
    results = vectorstore.similarity_search_with_score(
        question,
        k=k
    )

    relevant_documents = [
        doc
        for doc, distance in results
        if distance <= threshold
    ]

    return relevant_documents