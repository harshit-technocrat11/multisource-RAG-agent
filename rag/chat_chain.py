from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o",streaming=True)

system_prompt = ChatPromptTemplate.from_template("""
You are a multimodal RAG assitant, you will be provided contexts from different sources - pdf, csv, txt, website, image files , etc..

use only the context below to answer.

Context: 
{context}

Question:
{question}

If answer not in context, say "Not found in documents."
""")


def format_docs(docs):
    return "\n\n".join(
        f"[Page {d.metadata.get('page')}] {d.page_content}"
        for d in docs
    )


def answer_question_stream(retriever, query):

    docs = retriever.invoke(query)
    context = format_docs(docs)

    messages = system_prompt.format_messages(
        context=context,
        question=query
    )

    # Return token generator + sources
    stream = llm.stream(messages)

    return stream, docs