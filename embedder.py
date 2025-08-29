from google import genai
from google.genai.types import EmbedContentConfig

client = genai.Client()

def get_gemini_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text],
        config=EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"  # optional, helps optimize for RAG
        )
    )
    return response.embeddings[0].values
