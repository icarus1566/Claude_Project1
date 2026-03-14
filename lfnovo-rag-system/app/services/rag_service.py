from app.services.parser import DocumentParser
from app.services.chunker import DocumentChunker
from app.services.embedder import EmbedderService
from app.services.vector_store import VectorStoreService
from app.services.object_store import ObjectStoreService
from app.services.metadata_store import MetadataService
from app.services.ollama_client import OllamaClient
from app.core.config import settings
import uuid

class RAGService:
    def __init__(self):
        self.parser = DocumentParser()
        self.chunker = DocumentChunker()
        self.embedder = EmbedderService()
        self.vector_store = VectorStoreService(url=settings.QDRANT_URL)
        self.object_store = ObjectStoreService(
            settings.MINIO_ENDPOINT, settings.MINIO_ACCESS_KEY, 
            settings.MINIO_SECRET_KEY, settings.MINIO_BUCKET_NAME
        )
        self.metadata_store = MetadataService(settings.SQLALCHEMY_DATABASE_URI)
        self.llm = OllamaClient(settings.OLLAMA_BASE_URL, settings.LLM_MODEL)

    async def ingest_document(self, filename: str, file_bytes: bytes) -> str:
        doc_id = str(uuid.uuid4())
        
        # 1. 원본 저장
        s3_url = self.object_store.upload_file(f"{doc_id}_{filename}", file_bytes)
        self.metadata_store.create_document(doc_id, filename, s3_url)
        
        # 2. 파싱 및 청크화
        pages = self.parser.parse_pdf(file_bytes)
        chunks = self.chunker.chunk_text(pages)
        
        # 3. 임베딩 및 벡터스토어 삽입
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.embed_documents(texts)
        self.vector_store.insert_chunks(doc_id, chunks, embeddings)
        
        return doc_id

    async def query(self, user_query: str, top_k: int = 3):
        # 1. 쿼리 임베딩 및 검색
        query_emb = self.embedder.embed_queries([user_query])[0]
        results = self.vector_store.search(query_emb, top_k)
        
        sources = []
        context_texts = []
        for r in results:
            context_texts.append(r.payload["text"])
            sources.append({"text": r.payload["text"], "document_id": r.payload["document_id"], "score": r.score})
            
        # 2. 프롬프트 구성 및 LLM 호출
        context = "\n\n".join(context_texts)
        prompt = f"다음 문맥을 참고하여 질문에 답하세요.\n\n문맥:\n{context}\n\n질문: {user_query}\n\n답변:"
        
        answer = await self.llm.generate_response(prompt)
        return {"answer": answer, "sources": sources}
