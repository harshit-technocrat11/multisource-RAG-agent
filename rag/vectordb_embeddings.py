from langchain_community.vectorstores import FAISS  
from langchain_openai import OpenAIEmbeddings 
from rag.persistence import save_vectorstore

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-large")

# when docs passed , its converted into embeddings
def create_vectorstore(docs):

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    save_vectorstore(vectorstore) #saving it locally

    return vectorstore