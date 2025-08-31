import chromadb
from google import genai
from google.genai.types import EmbedContentConfig
import uuid
from config import get_api_key

# --- Initialize Chroma client ---
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create (or get) collection
collection = chroma_client.get_or_create_collection("my_collection")

# --- Initialize Gemini embedder ---
genai_client = genai.Client(api_key=get_api_key())

def get_gemini_embedding(text: str):
    try:
        # print("Inside embedding function")
        res = genai_client.models.embed_content(
            model="text-embedding-004",  # Updated model name
            contents=[{
                "parts": [{"text": text}]
            }],
            config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        # print("Embedding API response received",res.embeddings[0].values)
        return res.embeddings[0].values
    except Exception as e:
        print(f"Error getting embedding: {e}")
        # Return a dummy embedding as fallback
        return [0.0] * 768


# --- Add a message ---
def add_message(session_id: str, role: str, content: str):
    try:
        vector = get_gemini_embedding(content)
        # print("calling embedding API")
        doc_id = str(uuid.uuid4())

        collection.add(
            ids=[doc_id],
            embeddings=[vector],
            documents=[content],
            metadatas=[{"session_id": session_id, "role": role}]
        )
        return doc_id
    except Exception as e:
        print(f"Error adding message: {e}")
        return None


# --- Get conversation history by similarity ---
def get_history(query: str, session_id: str = None, top_k: int = 5):
    try:
        q_vec = get_gemini_embedding(query)

        # Apply optional filter by session_id
        where_filter = {"session_id": session_id} if session_id else None

        results = collection.query(
            query_embeddings=[q_vec],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas"]
        )

        # Results come as dict, return a friendlier format
        docs = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            docs.append({
                "role": meta["role"],
                "content": doc
            })
        return docs
    except Exception as e:
        print(f"Error getting history: {e}")
        return []


# --- Reset session (delete all messages for session_id) ---
def reset_session(session_id: str):
    try:
        collection.delete(where={"session_id": session_id})
    except Exception as e:
        print(f"Error resetting session: {e}")

def print_collection():
    print(collection.peek())
