import fitz  # PyMuPDF
from typing import List, Dict

class DocumentParser:
    def parse_pdf(self, file_bytes: bytes) -> List[Dict]:
        """PDF를 읽어 페이지별 텍스트를 추출합니다."""
        results = []
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text").strip()
            if text:
                results.append({"page": page_num + 1, "text": text})
        return results
