def get_retriever(vectordb, k=6):
    
    return vectordb.as_retriever(search_kwargs={"k":k})