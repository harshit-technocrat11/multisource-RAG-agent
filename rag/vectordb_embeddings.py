from langchain_community.vectorstores import FAISS  
from langchain_openai import OpenAIEmbeddings 

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-large")

def create_vectorstore(docs):
    embeddings = get_embeddings()
    return FAISS.from_documents(docs, embeddings)