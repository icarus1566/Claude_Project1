from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    result = await rag_service.query(request.query, request.top_k)
    return result
