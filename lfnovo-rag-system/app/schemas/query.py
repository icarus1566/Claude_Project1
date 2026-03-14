from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class SourceChunk(BaseModel):
    text: str
    document_id: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
