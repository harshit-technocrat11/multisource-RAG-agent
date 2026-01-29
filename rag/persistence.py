import os 
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

DB_PATH = "vectorDB"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# save locally
def save_vectorstore(vectorstore):
    vectorstore.save_local(DB_PATH)

# then load , if vectordb exists
def load_vectorstore():

    if os.path.exists(DB_PATH):
        return FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
)


    return None