# Windows 개발 환경 실행 가이드

## 1. 사전 준비
Docker Desktop 또는 Windows용 Podman Desktop 설치를 권장합니다.

## 2. 모델 폴더 세팅 (BGE-M3)
`models/embedding/bge-m3` 폴더에 HuggingFace에서 `BAAI/bge-m3`의 모델 파일들 (config.json, pytorch_model.bin 등)을 수동으로 다운로드 후 위치시킵니다. (오프라인 테스트용)

## 3. 서비스 구동
```powershell
docker-compose -f deploy/common/compose.yaml up -d
```
* Ollama에는 접속 후 초기 모델 풀(pull)이 필요합니다:
```bash
docker exec -it ollama ollama run llama3.1:8b
```
