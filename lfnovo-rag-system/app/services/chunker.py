from typing import List, Dict

class DocumentChunker:
    def chunk_text(self, pages: List[Dict], chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """간단한 고정 길이 기반 청킹 (고도화 시 LangChain TextSplitter 등으로 교체)"""
        chunks = []
        for page in pages:
            text = page["text"]
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunks.append({
                    "text": text[start:end],
                    "page": page["page"]
                })
                start = end - overlap
        return chunks
