from sentence_transformers import SentenceTransformer
from typing import List
import os

class EmbedderService:
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        # 폐쇄망의 경우 모델 경로를 오프라인 폴더로 지정
        offline_path = "/app/models/embedding/bge-m3"
        # 단순히 폴더만 있는게 아니라 핵심 설정 파일이 있는지 확인
        if os.path.exists(os.path.join(offline_path, "config.json")):
            model_name_or_path = offline_path
        else:
            model_name_or_path = model_name
            
        self.model = SentenceTransformer(model_name_or_path)
        
    def embed_queries(self, queries: List[str]) -> List[List[float]]:
        # BGE 모델의 경우 query 임베딩에 접두사나 특정 파라미터가 필요할 수 있음
        embeddings = self.model.encode(queries, normalize_embeddings=True)
        return embeddings.tolist()
        
    def embed_documents(self, docs: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(docs, normalize_embeddings=True)
        return embeddings.tolist()
