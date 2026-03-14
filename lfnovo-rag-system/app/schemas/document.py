from pydantic import BaseModel
from typing import List, Optional

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    message: Optional[str] = None

class ChunkMeta(BaseModel):
    chunk_id: str
    text: str
    page_number: int
