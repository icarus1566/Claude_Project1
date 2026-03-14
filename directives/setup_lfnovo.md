# SOP: lfnovo 환경 설정 및 모델 준비

이 문서는 Open Notebook (lfnovo) RAG 시스템을 안정적으로 배포하기 위한 표준 운영 절차(SOP)입니다.

## 1. 전제 조건
- Windows 환경에서 Docker Desktop 또는 OrbStack 설치 완료
- Python 3.10 이상 설치 완료
- `huggingface-cli` 설치 완료 (`pip install huggingface_hub`)

## 2. 모델 다운로드 (bge-m3)
API 서버가 구동되기 위해서는 임베딩 모델 가중치가 필요합니다.

1. **다운로드 실행**:
   ```powershell
   huggingface-cli download BAAI/bge-m3 --local-dir d:\ALL_AI\Claude_Project1\lfnovo-rag-system\models\embedding\bge-m3
   ```
   *참고: 이미 캐시가 존재할 경우, 위 명령어를 실행하면 필요한 파일만 매핑하여 빠르게 완료됩니다.*

2. **완료 확인**:
   `d:\ALL_AI\Claude_Project1\lfnovo-rag-system\models\embedding\bge-m3` 폴더 내에 `model.safetensors` 또는 `pytorch_model.bin` 파일이 있는지 확인하십시오.

## 3. 시스템 배포
Docker Compose를 사용하여 모든 서비스를 실행합니다.

1. **서비스 시작**:
   ```powershell
   docker compose -f d:\ALL_AI\Claude_Project1\lfnovo-rag-system\deploy\common\compose.yaml up -d
   ```

2. **상태 확인 (자동화)**:
   `execution/docker_manage.py` 스크립트를 사용하여 서비스 상태를 점검합니다.
   ```powershell
   python d:\ALL_AI\Claude_Project1\execution\docker_manage.py --check-health
   ```

## 4. 문제 해결 (8000번 포트 연결 불가)
포트 8000번 접근이 안 될 경우 다음을 확인합니다:
- **로그 확인**: `docker logs rag-api`
- **모델 경로**: 컨테이너 내 `/app/models/embedding/bge-m3` 경로에 파일이 올바르게 마운트되었는지 확인.
- **포트 충돌**: `netstat -ano | findstr :8000` 명령어로 다른 프로세스가 포트를 점유 중인지 확인.
