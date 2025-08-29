# vector_utils.py

from redisvl.index import SearchIndex
from redisvl.schema import IndexSchema
from redisvl.query import VectorQuery
from redisvl.utils.vectorize import VertexAITextVectorizer
from google import genai
from google.genai.types import EmbedContentConfig

# Initialize Gemini embedder
genai_client = genai.Client()
def get_gemini_embedding(text: str):
    res = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text],
        config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return res.embeddings[0].values

# Configure RedisVL index
schema = {
    "index": {
        "name": "chat_history_index",
        "prefix": "chat:",
    },
    "fields": [
        {"name": "session_id", "type": "tag"},
        {"name": "role", "type": "text"},
        {"name": "content", "type": "text"},
        {"name": "embedding", "type": "vector", "attrs": {"dims": 768, "algorithm": "flat", "distance_metric": "cosine"}},
    ],
}
index = SearchIndex.from_dict(schema)
index.connect()
index.create()

def add_message(session_id: str, role: str, content: str):
    vector = get_gemini_embedding(content)
    doc = {"session_id": session_id, "role": role, "content": content, "content_vector": vector}
    index.load([doc], id_field="session_id")

def get_history(query: str, session_id: str = None, top_k: int = 5):
    q_vec = get_gemini_embedding(query)
    fq = f"@session_id:{{{session_id}}}" if session_id else None
    results = index.query(VectorQuery(vector=q_vec, top_k=top_k, return_fields=["role", "content"], filter_expression=fq))
    return results.docs

def reset_session(session_id: str):
    index.delete_by_query(f"@session_id:{{{session_id}}}")
