class ContextBuilder:
    def build(
        self,
        retrieval_results: list[dict],
    ) -> str:

        if not retrieval_results:
            return ""

        context_chunks = []

        for result in retrieval_results:
            text = result.get("text", "").strip()

            if not text:
                continue

            document_id = result.get("document_id", "unknown")
            page_number = result.get("page_number", "unknown")
            chunk_index = result.get("chunk_index", "unknown")
            score = result.get("score", 0.0)

            formatted_chunk = (
                f"[Doc: {document_id} | Page: {page_number} | Chunk: {chunk_index} | Score: {score:.4f}]\n"
                f"{text}"
            )

            context_chunks.append(formatted_chunk)

        return "\n\n".join(context_chunks)
