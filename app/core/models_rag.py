from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentChunk(BaseModel):
    content: str
    source_id: str
    chunk_index: int
    metadata: dict = Field(default_factory=dict)

class IngestRequest(BaseModel):
    text: str
    filename: str
    meta: Optional[dict] = {}

class QueryRequest(BaseModel):
    query: str
    limit: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence_score: Optional[float] = None
