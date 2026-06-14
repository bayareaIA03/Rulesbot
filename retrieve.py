import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "chroma_db"
COLLECTION_NAME = "csueb_professor_reviews"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query, k=5):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
    ):
        retrieved_chunks.append({
            "text": document,
            "filename": metadata.get("filename", ""),
            "source_name": metadata.get("source_name", ""),
            "chunk_index": metadata.get("chunk_index", ""),
            "distance": distance
        })

    return retrieved_chunks


if __name__ == "__main__":
    query = input("Ask a question: ")
    chunks = retrieve(query)

    print("\nTop retrieved chunks:")
    for chunk in chunks:
        print("\n---")
        print("Source:", chunk["filename"])
        print("Chunk index:", chunk["chunk_index"])
        print("Distance:", chunk["distance"])
        print(chunk["text"])