# SOP: lfnovo 시스템 이전 및 신규 설치 가이드

이 문서는 기존 컴퓨터에서 구동 중인 lfnovo RAG 시스템을 아무것도 설치되지 않은 신규 노트북으로 이전하는 절차를 설명합니다.

## 1. 신규 노트북 준비 (사전 설치)
새 노트북에서 다음 프로그램을 순서대로 설치해야 합니다.

1. **Docker Desktop 설치**: [docker.com](https://www.docker.com/products/docker-desktop/)에서 다운로드 및 설치.
2. **Python 설치**: [python.org](https://www.python.org/)에서 3.10 이상 버전 설치 (설치 시 'Add Python to PATH' 옵션 필수 선택).
3. **Ollama 설치 (선택 사항)**: 로컬 LLM 구동을 원할 경우 [ollama.com](https://ollama.com/)에서 설치.

## 2. 파일 복사 (압축 및 이동)
가장 효율적인 방법은 외장 하드나 대용량 USB를 사용하는 것입니다.

1. **복사할 폴더**:
   - `d:\ALL_AI\Claude_Project1` 전체 폴더
   - **중요**: `lfnovo-rag-system\models` 폴더는 용량이 매우 크므로(수 GB), 반드시 포함되어 있는지 확인하십시오. (이 폴더가 있으면 새 노트북에서 다시 다운로드할 필요가 없습니다.)
   
2. **붙여넣기 경로**:
   - 새 노트북에서도 가급적 동일한 경로(`d:\ALL_AI\Claude_Project1`)를 권장하지만, 환경에 따라 `C:\` 드라이브 등으로 변경 가능합니다. (이 경우 스크립트 내 경로 수정이 필요할 수 있습니다.)

## 3. 환경 복구 및 실행
파일 복사가 완료된 후 새 노트북에서 다음 과정을 수행합니다.

1. **Docker Desktop 실행**: 엔진이 완전히 켜질 때까지 기다립니다.
2. **파이썬 라이브러리 설치** (필요한 경우):
   ```powershell
   pip install huggingface_hub
   ```
3. **시스템 가동**:
   `execution\docker_manage.py` 스크립트를 사용하여 서비스를 시작합니다.
   ```powershell
   python [복사한경로]\execution\docker_manage.py --restart
   ```

## 4. 확인 및 검증
브라우저를 열어 다음 주소에 접속되는지 확인합니다.
- Open WebUI: `http://localhost:3000`
- API Health: `http://localhost:8000/api/v1/health`

---
> [!TIP]
> 모델 파일(`bge-m3`)을 복사하는 것이 가장 핵심입니다. 인터넷 속도가 느린 환경이라면 복사하는 것이 다운로드보다 훨씬 빠릅니다.
