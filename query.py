
import os
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def format_context(chunks):
    """
    Format retrieved chunks into a context block for the LLM.
    Each chunk includes the source filename so the answer can be grounded.
    """
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        source = chunk.get("filename", "unknown source")
        text = chunk.get("text", "")

        context_parts.append(
            f"Source {i}: {source}\n{text}"
        )

    return "\n\n".join(context_parts)


def ask(question):
    """
    Full RAG flow:
    1. Retrieve relevant chunks
    2. Send chunks to Groq Llama model
    3. Generate a grounded answer
    4. Return answer and sources
    """
    retrieved_chunks = retrieve(question, k=5)
    context = format_context(retrieved_chunks)

    prompt = f"""
You are a grounded question-answering assistant for CSU East Bay professor and course reviews.

Use only the provided context to answer the question.

Rules:
1. Answer only from the provided context.
2. Do not use outside knowledge.
3. If the context does not contain enough information, say exactly:
   "I don't have enough information from the provided documents."
4. Cite the source filename in your answer.
5. Keep the answer clear and concise.
6. Do not make claims that are not supported by the retrieved chunks.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    sources = sorted(
        set(chunk.get("filename", "unknown source") for chunk in retrieved_chunks)
    )

    return {
        "answer": answer,
        "sources": sources,
        "chunks": retrieved_chunks
    }


if __name__ == "__main__":
    question = input("Ask a question: ")

    result = ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources retrieved:")
    for source in result["sources"]:
        print("-", source)


