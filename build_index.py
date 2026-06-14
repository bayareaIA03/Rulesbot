import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "chunks.json"
DB_PATH = "chroma_db"
COLLECTION_NAME = "csueb_professor_reviews"


def main():
    print("Loading chunks...")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=DB_PATH)

    # Delete old collection if it exists, so reruns do not duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        metadatas.append({
            "source_name": chunk.get("source_name", ""),
            "filename": chunk.get("filename", ""),
            "chunk_index": chunk.get("chunk_index", 0)
        })

    print("Creating embeddings...")
    embeddings = model.encode(documents).tolist()

    print("Saving to ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Saved {len(documents)} chunks to ChromaDB collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()