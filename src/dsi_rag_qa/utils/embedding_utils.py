import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_EMBEDDINGS = OllamaEmbeddings(model="bge-m3")

def create_faiss_retriever(docs, embeddings=DEFAULT_EMBEDDINGS, chunk_size=1000, chunk_overlap=200, search_k=5):
    """
    Create a FAISS vector store from the provided documents using the specified embeddings.
    
    Args:
        docs (list): List of documents to be embedded and stored.
        embeddings: Embeddings model to use for vectorization.
        chunk_size (int): Size of each text chunk.
        chunk_overlap (int): Overlap between chunks.
    
    Returns:
        FAISS: A FAISS vector store containing the embedded documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(docs)
    
    vector_store = FAISS.from_documents(texts, embeddings)

    vector_retriever = vector_store.as_retriever(search_kwargs={"k": search_k})

    return vector_retriever, vector_store

