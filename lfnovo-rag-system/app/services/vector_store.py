from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict
import uuid

class VectorStoreService:
    def __init__(self, url: str, collection_name: str = "documents"):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self._ensure_collection()
        
    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            # BGE-M3는 일반적으로 1024차원을 사용
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
            
    def insert_chunks(self, document_id: str, chunks: List[Dict], embeddings: List[List[float]]):
        points = []
        for chunk, emb in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=emb,
                    payload={"document_id": document_id, "text": chunk["text"], "page": chunk["page"]}
                )
            )
        self.client.upsert(collection_name=self.collection_name, points=points)
        
    def search(self, query_embedding: List[float], top_k: int = 3):
        # qdrant-client 1.10+ 최신 API (query_points) 사용
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k
        )
        return response.points
