from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150
)

# central chunker 
def chunk_docs(docs):
    chunked=[]

    for doc in docs:
        chunks = splitter.split_text(doc.page_content)

        for c in chunks:
            chunked.append(
                doc.__class__(
                    page_content=c,
                    metadata=doc.metadata
                )
            )
    return chunked