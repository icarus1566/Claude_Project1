from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.schemas.document import DocumentResponse
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    # 대규모 로드 시 BackgroundTasks를 활용, MVP에서는 blocking 혹은 async 직접 대기 처리
    doc_id = await rag_service.ingest_document(file.filename, file_bytes)
    return DocumentResponse(document_id=doc_id, filename=file.filename, status="success")
