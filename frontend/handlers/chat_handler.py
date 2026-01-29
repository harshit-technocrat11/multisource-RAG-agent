from rag.chat_chain import answer_question_stream

def handle_chat(retriever, query):

    stream, sources = answer_question_stream(
        retriever,
        query
    )

    streamed_text = ""

    for chunk in stream:
        if chunk.content:
            streamed_text += chunk.content

    unique_sources = {}

    for s in sources:
        src = s.metadata.get("source")
        loc = s.metadata.get("page", s.metadata.get("row", "N/A"))

        if src not in unique_sources:
            unique_sources[src] = set()

        unique_sources[src].add(loc)

    source_text = "\n".join(
        f"{src} (locations: {', '.join(map(str, locs))})"
        for src, locs in unique_sources.items()
    )

    final_answer = f"{streamed_text}\n\n📌 Sources:\n{source_text}"

    return final_answer
