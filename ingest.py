import os
import json
import re

DOCS_PATH = "data"
OUTPUT_FILE = "chunks.json"


def clean_text(text):
    """
    Clean the raw professor review text before chunking.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    return text.strip()


def load_documents():
    """
    Load all .txt professor review documents from the data folder.
    """
    documents = []

    if not os.path.exists(DOCS_PATH):
        print(f"ERROR: Folder '{DOCS_PATH}' not found.")
        return documents

    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            source_name = filename.replace(".txt", "").replace("_", " ").title()

            documents.append({
                "source_name": source_name,
                "filename": filename,
                "text": clean_text(text),
            })

    print(f"Loaded {len(documents)} document(s): {[d['filename'] for d in documents]}")
    return documents


def chunk_document(text, source_name, filename):
    """
    Split one professor review document into chunks ready for embedding.

    Strategy:
    - chunk_size = 700 characters
    - overlap = 100 characters
    - min_length = 50 characters

    This fits professor review text because reviews are usually short,
    opinion-based, and focused on teaching style, workload, grading, or class experience.
    """
    chunk_size = 500
    overlap = 100
    min_length = 50

    chunks = []
    prefix = filename.replace(".txt", "")
    counter = 0

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "source_name": source_name,
                "filename": filename,
                "chunk_id": f"{prefix}_{counter}",
                "chunk_index": counter,
            })
            counter += 1

        start += chunk_size - overlap

    return chunks


def main():
    print("Starting ingestion...")

    documents = load_documents()

    if not documents:
        print("No documents found. Make sure your .txt files are inside the data folder.")
        return

    all_chunks = []

    for document in documents:
        chunks = chunk_document(
            document["text"],
            document["source_name"],
            document["filename"]
        )
        all_chunks.extend(chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nCreated {len(all_chunks)} chunk(s)")
    print(f"Saved chunks to {OUTPUT_FILE}")

    print("\nSample chunks:")
    for chunk in all_chunks[:5]:
        print("\n---")
        print("Source:", chunk["filename"])
        print("Chunk ID:", chunk["chunk_id"])
        print(chunk["text"])


if __name__ == "__main__":
    main()