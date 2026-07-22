from groq import Groq

from src.config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
)


class GroqGenerator:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:

        if not context.strip():
            return "I could not find the answer in the provided documents."

        prompt = f"""
You are a retrieval-augmented assistant.

You must follow these rules strictly:

1. Use ONLY the provided context.
2. If the answer is not in the context, say:
   "I could not find the answer in the provided documents."
3. When answering, use the metadata in the context:
   - Document ID
   - Page number
   - Chunk index
4. Do NOT guess or use external knowledge.
5. If relevant, mention the page number in your reasoning.

Context:
{context}

Question:
{question}

Answer format:
- Clear and direct answer
- Optionally include: (Source: Doc X, Page Y)
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict RAG system. "
                        "You must only use provided context and respect citations."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            max_completion_tokens=1024,
        )

        return (response.choices[0].message.content or "").strip()
