import chromadb
from chromadb.utils import embedding_functions
from app.core.settings import get_settings
from app.core.models_rag import DocumentChunk
from typing import List
import uuid

settings = get_settings()

class RAGService:
    def __init__(self):
        # Persistent Client: Stores data in ./data/chroma
        self.chroma_client = chromadb.PersistentClient(path="./data/chroma")
        
        # Use OpenAI Embeddings
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name="text-embedding-3-small"
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=self.openai_ef
        )

    def ingest_text(self, text: str, filename: str):
        """
        Splits text into chunks and saves to Vector DB.
        """
        # Simple chunking strategy (character based for V1)
        chunk_size = 1000
        overlap = 100
        
        chunks = []
        ids = []
        metadatas = []
        
        start = 0
        text_len = len(text)
        
        i = 0
        while start < text_len:
            end = start + chunk_size
            chunk_content = text[start:end]
            
            chunks.append(chunk_content)
            ids.append(str(uuid.uuid4()))
            metadatas.append({"source": filename, "chunk_index": i})
            
            start += (chunk_size - overlap)
            i += 1
            
        if chunks:
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Ingested {len(chunks)} chunks from {filename}")

    def search(self, query: str, limit: int = 3) -> List[str]:
        """
        Semantic search for relevant chunks.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        # Flatten results (Chroma returns list of lists)
        if results and results['documents']:
            return results['documents'][0]
        return []
